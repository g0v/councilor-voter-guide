for ii in $(ls | grep cc$ ) ;do echo $ii &&cd $ii && python deploy.py && cd .. ; done

