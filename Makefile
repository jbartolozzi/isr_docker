SHELL:=/bin/bash

dockerfile := "Dockerfile"
tag_name := "jhb_isr"
build:
	USER_ID=$(UID) docker build -f ./$(dockerfile) -t $(tag_name) ./
shell:
	docker run --gpus all --entrypoint /bin/bash -v $(pwd):/input -w /input --rm -it -v `pwd`:/input -t $(tag_name) 
clean:
	docker rmi $(tag_name)