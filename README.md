# isr_docker
Tiny helper for running ISR through Docker

Run build using make file (```make build```)
add alias
```alias isr='docker run --gpus all -v $(pwd):/input -w /input --rm -it -v `pwd`:/input -t jhb_isr $@'```
