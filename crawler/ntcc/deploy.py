
import os
project_name = os.getcwd().split("/")[-1]

assert "G0V_PORT" in os.environ, "please --link g0v:g0v"

scrapy_url = os.environ["G0V_PORT"]
scrapy_url = scrapy_url.replace("tcp","http")
cfg = '''[settings]\ndefault = {project_name}.settings\n\n[deploy]\nurl = {deploy_url}\nproject = {project_name}'''

with open("scrapy.cfg","w") as wf:
    wf.write(cfg.format(project_name=project_name,deploy_url=scrapy_url))

os.system("scrapy deploy")


