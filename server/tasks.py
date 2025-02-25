from invoke import task

@task
def dev(c, port=5000):
    cmd = f"PYTHONPATH=$(pwd) FLASK_DEBUG=1 flask --app application:application run --host 0.0.0.0 --port {port}"
    c.run(cmd, hide=False, warn=True)
