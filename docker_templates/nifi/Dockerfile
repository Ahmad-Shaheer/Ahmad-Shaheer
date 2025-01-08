FROM apache/nifi:latest

# Create a directory for the custom drivers
USER root
RUN mkdir /opt/nifi/drivers
COPY drivers/*.jar /opt/nifi/drivers/
RUN chown -R nifi:nifi /opt/nifi/drivers

# Switch back to the nifi user
USER nifi

# Update NiFi configuration (optional) to load custom driver directory
# This can be done via nifi.properties or via the UI later.
# For simplicity, we won't modify configs here, but you can ensure NiFi sees these drivers 
# by placing them in 'NIFI_HOME/lib' or configuring DBCPConnectionPoolControllers to use them.

# If you want them in NiFi's lib directory:
RUN cp /opt/nifi/drivers/*.jar /opt/nifi/nifi-current/lib/

