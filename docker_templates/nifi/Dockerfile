FROM apache/nifi:latest

# Create a directory for the custom drivers
USER root
RUN mkdir /opt/nifi/drivers
COPY drivers/*.jar /opt/nifi/drivers/
RUN chown -R nifi:nifi /opt/nifi/drivers
# Switch back to the nifi user
USER nifi
# If you want them in NiFi's lib directory:
RUN cp /opt/nifi/drivers/*.jar /opt/nifi/nifi-current/lib/

