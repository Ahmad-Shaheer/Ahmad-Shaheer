import subprocess
import json
import os
import shutil
import yaml
from typing import List, Dict, Tuple, Union


class DockerManager:
    """
    Handles Docker commands (up/down) and merges Docker Compose files.
    Preserves the exact logic from the original procedural functions.
    """

    def run_docker_compose(self) -> None:
        """
        Runs the `docker compose up` command to build and start all services.
        
        Executes the Docker Compose file to build and bring up containers.
        Handles any errors during execution.

        Raises:
            subprocess.CalledProcessError: If the command fails.
        """
        try:
            command = "docker compose up --build"
            result = subprocess.run(f"sudo {command}", shell=True, check=True)

            if result.stderr:
                print("Error:\n", result.stderr)

        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            print("Error Output:", e.stderr)

    def down_docker_compose(self) -> None:
        """
        Runs the `docker compose down` command to stop and remove containers, networks, and volumes.

        Raises:
            subprocess.CalledProcessError: If the command fails.
        """
        try:
            command = "docker compose down -v"
            result = subprocess.run(f"sudo {command}", shell=True, check=True)

            if result.stderr:
                print("Error:\n", result.stderr)

        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            print("Error Output:", e.stderr)

    def check_containers_health(self) -> Tuple[Union[bool, str], List[str]]:
        """
        Checks the health status of all running Docker containers.

        Returns:
            Tuple[Union[bool, str], List[str]]:
                - "no_containers": If no containers are running.
                - (True, [healthy_container_names]): If all running containers are healthy.
                - (False, [healthy_container_names]): If not all containers are healthy.
                  The list contains names of healthy containers, which may be empty if none are healthy.
        """
        ps_cmd = ["sudo", "docker", "ps", "-q"]
        try:
            result = subprocess.run(ps_cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print("Error running docker ps:", e.stderr)
            return False, []

        container_ids = result.stdout.strip().split()
        if not container_ids:
            return False, []

        healthy_containers = []
        for container_id in container_ids:
            inspect_cmd = ["sudo", "docker", "inspect", container_id]
            try:
                inspect_result = subprocess.run(
                    inspect_cmd, capture_output=True, text=True, check=True
                )
            except subprocess.CalledProcessError as e:
                print(f"Error inspecting container {container_id}:", e.stderr)
                continue  # skip this container

            try:
                data = json.loads(inspect_result.stdout)
                container_info = data[0] if data else {}
                container_name = container_info.get("Name", "").lstrip("/")
                state = container_info.get("State", {})
                health = state.get("Health", {})
                health_status = health.get("Status")
                if health_status == "healthy":
                    healthy_containers.append(container_name)
            except (json.JSONDecodeError, IndexError, KeyError) as e:
                print(f"Error parsing JSON for container {container_id}:", e)
                continue

        if len(healthy_containers) == len(container_ids):
            return True, healthy_containers
        else:
            return False, healthy_containers

    def merge_docker_compose(self, tool_names: List[str], base_directory: str = "docker_templates") -> Dict[str, List[str]]:
        """
        Merges Docker Compose files from multiple tools into a single Compose file.

        Args:
            tool_names (List[str]): List of tool names whose Docker Compose files need to be merged.
            base_directory (str): Directory containing Docker Compose files for each tool.
                                  Defaults to "docker_templates".

        Returns:
            Dict[str, List[str]]: A dictionary of port assignments for each service.
                                  Keys are service names, values are lists of assigned ports.

        Process:
            - Reads `docker-compose.yml` files from the specified tools.
            - Handles service name conflicts by renaming services.
            - Resolves port conflicts by assigning available ports.
            - Merges volume mounts, network configurations, and environment variables.
            - Detects conflicts in environment variable assignments across services.
            - Writes the merged Compose file as `docker-compose.yml`.

        Raises:
            yaml.YAMLError: If a YAML parsing error occurs.
            OSError: If file/directory operations fail during volume handling.
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

        allocated_ports = {}
        port_assignments = {}
        temp_merged_volumes = "temp_merged_volumes"
        os.makedirs(temp_merged_volumes, exist_ok=True)
        all_service_envs = {}
        used_service_names = set()

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
                if service_name in used_service_names:
                    new_service_name = f"{tool_name.lower()}_{service_name}"
                    print(f"Service name conflict detected for '{service_name}'. "
                          f"Renaming to '{new_service_name}'")
                else:
                    new_service_name = service_name

                used_service_names.add(new_service_name)
                merged_compose['services'][new_service_name] = service_config.copy()

                # Handle custom build or image references
                if has_dockerfile and 'build' in service_config:
                    build_value = service_config['build']
                    if isinstance(build_value, dict):
                        merged_compose['services'][new_service_name]['build']['context'] = tool_dir
                    elif isinstance(build_value, str):
                        merged_compose['services'][new_service_name]['build'] = {
                            'context': os.path.join(tool_dir, build_value)
                        }
                    else:
                        print(f"Warning: 'build' format for '{new_service_name}' is unrecognized.")
                else:
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

                # --- 6. Handle depends_on references ---
                if 'depends_on' in service_config:
                    depends_config = service_config['depends_on']
                    if isinstance(depends_config, dict):
                        new_depends = {}
                        for dep_service, dep_config in depends_config.items():
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

                # --- 7. Collect environment variables ---
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

        # Detect environment variable conflicts
        env_conflicts = {}
        for service_name, envs in all_service_envs.items():
            for k, v in envs.items():
                env_conflicts.setdefault(k, {}).setdefault(v, []).append(service_name)

        for env_var, values_dict in env_conflicts.items():
            if len(values_dict) > 1:
                print(f"Warning: Conflict detected for ENV variable '{env_var}':")
                for val, services in values_dict.items():
                    print(f"  Value '{val}' set by services: {services}")

        # Write the merged Docker Compose file
        with open("docker-compose.yml", 'w') as outfile:
            yaml.dump(merged_compose, outfile, sort_keys=False, indent=2)

        return port_assignments
