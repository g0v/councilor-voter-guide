
import os
project_name = os.getcwd().split("/")[-1]

assert "G0V_PORT" in os.environ, "please --link g0v:g0v"

scrapy_url = os.environ["G0V_PORT"]
scrapy_url = scrapy_url.replace("tcp","http")

project_name = "tcc"

os.system("curl {scrapy_url}/schedule.json -d project={project_name} -d spider=bills -d setting=LOG_LEVEL=DEBUG".format(scrapy_url=scrapy_url,project_name=project_name))
os.system("curl {scrapy_url}/schedule.json -d project={project_name} -d spider=councilors -d setting=LOG_LEVEL=DEBUG".format(scrapy_url=scrapy_url,project_name=project_name))
os.system("curl {scrapy_url}/schedule.json -d project={project_name} -d spider=councilors_terms -d setting=LOG_LEVEL=DEBUG".format(scrapy_url=scrapy_url,project_name=project_name))
os.system("curl {scrapy_url}/schedule.json -d project={project_name} -d spider=councilors_terms -d setting=LOG_LEVEL=DEBUG".format(scrapy_url=scrapy_url,project_name=project_name))



