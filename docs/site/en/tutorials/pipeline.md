# What is a pipeline?
The Phantoscope project uses pipeline to link operators together. A pipeline is an abstract of an data process.

A pipeline controls the flow of a data processing process. It transfers the output of an operator to the next operator down the line. 

Following are some golden rules you should follow when designing a pipeline: 

- A pipeline can only have one encoder. 
- A pipeline can have no processor. 
- A pipeline must have an encoder. 
- The input to an pipeline must meet the requirements of its first operator. 