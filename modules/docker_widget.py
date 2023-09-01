from libqtile.widget.base import InLoopPollText
import subprocess


class DockerWidget(InLoopPollText):

    def __init__(self, **config):
        InLoopPollText.__init__(self, default_text='TEST', **config)

    def poll(self):
        docker_ps = subprocess.run('docker ps', shell=True, capture_output=True).stdout.decode()
        containers = len(docker_ps.split('\n')) - 2
        
        return f'running containers: {containers}'

