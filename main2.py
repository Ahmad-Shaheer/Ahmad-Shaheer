#!/usr/bin/env python3
import os
import shutil
import yaml

def merge_docker_compose(tool_names, base_directory="docker_templates"):
    """
    Merges docker-compose.yml files from multiple tools into a single Compose file.
    Handles port conflicts, merges volumes, and detects environment variable conflicts.
    """

    # Initialize the merged Compose structure
    merged_compose = {
        'version': '3.9',
        'services': {},
        'networks': {
            'data_pipeline_network': {}
        },
        'volumes': {}
    }

    # Dictionary for allocated host ports => service
    allocated_ports = {}

    # Store final (host:container) port assignments for each service
    port_assignments = {}

    # Temporary directory for merging volume contents
    temp_merged_volumes = "temp_merged_volumes"
    os.makedirs(temp_merged_volumes, exist_ok=True)

    # For detecting environment variable conflicts across services
    # Structure: {service_name: {env_key: env_value, ...}}
    all_service_envs = {}

    # ------------------------------------------------------------
    # NEW: Track used service names so we only prefix if there's a conflict
    used_service_names = set()
    # ------------------------------------------------------------

    for tool_name in tool_names:
        tool_dir = os.path.join(base_directory, tool_name.lower())
        compose_file_path = os.path.join(tool_dir, "docker-compose.yml")

        # --- 1. Read the Tool's docker-compose.yml ---
        if not os.path.exists(compose_file_path):
            print(f"Warning: Compose file not found for tool '{tool_name}': {compose_file_path}")
            continue

        with open(compose_file_path, 'r') as f:
            try:
                tool_compose = yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML for tool '{tool_name}': {e}")
                continue

        if not tool_compose or 'services' not in tool_compose:
            print(f"Warning: No services defined in {compose_file_path}")
            continue

        # --- 2. Check if the tool has a custom Dockerfile ---
        has_dockerfile = os.path.exists(os.path.join(tool_dir, "Dockerfile"))

        # --- 3. Merge Services ---
        for service_name, service_config in tool_compose['services'].items():

            # ------------------------------------------------------------
            # CHANGE: Check if this service_name is already used
            if service_name in used_service_names:
                # Conflict -> rename + print message
                new_service_name = f"{tool_name.lower()}_{service_name}"
                print(f"Service name conflict detected for '{service_name}'. Renaming to '{new_service_name}'")
            else:
                # No conflict -> keep name as-is
                new_service_name = service_name

            # Add the final name to the used_service_names
            used_service_names.add(new_service_name)
            # ------------------------------------------------------------

            merged_compose['services'][new_service_name] = service_config.copy()

            # Handle custom build or image references
            if has_dockerfile and 'build' in service_config:
                build_value = service_config['build']
                if isinstance(build_value, dict):
                    # Dictionary form
                    merged_compose['services'][new_service_name]['build']['context'] = tool_dir
                elif isinstance(build_value, str):
                    # String form -> convert to dict
                    merged_compose['services'][new_service_name]['build'] = {
                        'context': os.path.join(tool_dir, build_value)
                    }
                else:
                    # If it's something else, just warn
                    print(f"Warning: 'build' format for '{new_service_name}' is unrecognized.")
            else:
                # If no Dockerfile, we expect an image field or something else
                if 'image' not in service_config:
                    print(f"Warning: Service '{new_service_name}' has no 'image' or 'build' definition.")

            # --- 4. Handle Volume Mounts ---
            if 'volumes' in service_config:
                new_volume_list = []
                for vol in service_config['volumes']:
                    if isinstance(vol, str):
                        parts = vol.split(':')
                        if len(parts) == 2:
                            source, dest = parts
                            if source.startswith('./') or os.path.isdir(os.path.join(tool_dir, source)):
                                abs_source_path = os.path.join(tool_dir, source)
                                merged_volume_dir = os.path.join(
                                    temp_merged_volumes,
                                    f"{tool_name.lower()}_{service_name}_{os.path.basename(source.strip('./'))}"
                                )
                                if os.path.exists(abs_source_path):
                                    if os.path.isdir(abs_source_path):
                                        try:
                                            shutil.copytree(abs_source_path, merged_volume_dir, dirs_exist_ok=True)
                                        except OSError:
                                            print(f"Skipping copy for {abs_source_path}: Directory not found.")
                                    else:
                                        # Single file
                                        if os.path.isfile(abs_source_path):
                                            os.makedirs(merged_volume_dir, exist_ok=True)
                                            shutil.copy2(abs_source_path, merged_volume_dir)
                                        else:
                                            print(f"Skipping {abs_source_path}, not found.")
                                new_volume_list.append(f"{os.path.abspath(merged_volume_dir)}:{dest}")
                            else:
                                # Named volume, prefix with tool+service
                                volume_name = f"{tool_name.lower()}_{service_name}_{source}"
                                merged_compose['volumes'][volume_name] = {}
                                new_volume_list.append(f"{volume_name}:{dest}")
                        else:
                            new_volume_list.append(vol)
                    elif isinstance(vol, dict):
                        for k, v in vol.items():
                            volume_name = f"{tool_name.lower()}_{service_name}_{k}"
                            merged_compose['volumes'][volume_name] = {}
                            new_volume_list.append({volume_name: v})
                    else:
                        new_volume_list.append(vol)

                merged_compose['services'][new_service_name]['volumes'] = new_volume_list

            # Add the service to the shared network
            merged_compose['services'][new_service_name]['networks'] = ['data_pipeline_network']

            # --- 5. Handle Port Conflicts ---
            if 'ports' in service_config:
                updated_ports = []
                for port_mapping in service_config['ports']:
                    host_port = None
                    container_port = None

                    if isinstance(port_mapping, str):
                        parts = port_mapping.split(':')
                        if len(parts) == 2:
                            host_port_str, container_port_str = parts
                            host_port = int(host_port_str)
                            container_port = int(container_port_str)
                    elif isinstance(port_mapping, int):
                        host_port = port_mapping
                        container_port = port_mapping
                    elif (isinstance(port_mapping, dict)
                          and 'published' in port_mapping
                          and 'target' in port_mapping):
                        host_port = int(port_mapping['published'])
                        container_port = int(port_mapping['target'])

                    if host_port is not None:
                        while host_port in allocated_ports:
                            host_port += 1  # increment until free

                        allocated_ports[host_port] = new_service_name

                        if isinstance(port_mapping, str):
                            updated_ports.append(f"{host_port}:{container_port}")
                            port_assignments.setdefault(new_service_name, []).append(f"{host_port}:{container_port}")
                        elif isinstance(port_mapping, int):
                            updated_ports.append(host_port)
                            port_assignments.setdefault(new_service_name, []).append(str(host_port))
                        elif isinstance(port_mapping, dict):
                            new_port_mapping = {
                                'published': host_port,
                                'target': container_port
                            }
                            for extra_key in ['protocol', 'mode']:
                                if extra_key in port_mapping:
                                    new_port_mapping[extra_key] = port_mapping[extra_key]

                            updated_ports.append(new_port_mapping)
                            port_assignments.setdefault(new_service_name, []).append(f"{host_port}:{container_port}")

                merged_compose['services'][new_service_name]['ports'] = updated_ports

            # --- 6. Handle depends_on references, prefixing those too ---
            if 'depends_on' in service_config:
                depends_config = service_config['depends_on']

                if isinstance(depends_config, dict):
                    new_depends = {}
                    for dep_service, dep_config in depends_config.items():
                        # If the original dep_service was renamed, we need to look up
                        # how we stored it. But for simplicity, we'll just prefix it
                        # the same way we do for volumes or do no prefix at all.
                        # If you want advanced logic, see how you handle the rename.
                        if dep_service in used_service_names:
                            new_depends[dep_service] = dep_config
                        else:
                            new_depends[dep_service] = dep_config
                    merged_compose['services'][new_service_name]['depends_on'] = new_depends

                elif isinstance(depends_config, list):
                    new_depends_list = []
                    for dep_service in depends_config:
                        if dep_service in used_service_names:
                            new_depends_list.append(dep_service)
                        else:
                            new_depends_list.append(dep_service)
                    merged_compose['services'][new_service_name]['depends_on'] = new_depends_list

            # --- 7. Accumulate environment variables for conflict detection ---
            env_vars = merged_compose['services'][new_service_name].get('environment', {})
            if isinstance(env_vars, list):
                env_dict = {}
                for env_item in env_vars:
                    if '=' in env_item:
                        k, v = env_item.split('=', 1)
                        env_dict[k] = v
                env_vars = env_dict

            if not isinstance(env_vars, dict):
                env_vars = {}

            all_service_envs[new_service_name] = env_vars

    env_conflicts = {}
    for service_name, envs in all_service_envs.items():
        for k, v in envs.items():
            env_conflicts.setdefault(k, {}).setdefault(v, []).append(service_name)

    for env_var, values_dict in env_conflicts.items():
        if len(values_dict) > 1:
            print(f"Warning: Conflict detected for ENV variable '{env_var}':")
            for val, services in values_dict.items():
                print(f"  Value '{val}' set by services: {services}")

    # --- 9. Write the merged Docker Compose file ---
    with open("docker-compose.yml", 'w') as outfile:
        yaml.dump(merged_compose, outfile, sort_keys=False, indent=2)

   
    return port_assignments

    


if __name__ == "__main__":
    
    tools_to_merge = ["NIFI", "MongoDB", "Spark", "Hadoop", "airflow"]
    
    merge_docker_compose(tools_to_merge)
