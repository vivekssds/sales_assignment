WORKDIR /work_dir
COPY requirements.txt /work_dir/
RUN pip install -r requirements.txt
COPY scripts_airflow/ /project/scripts/
RUN chmod +x /project/scripts/init.sh
ENTRYPOINT [ "/project/scripts/init.sh" ]