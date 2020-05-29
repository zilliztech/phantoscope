# What is an operator?
An operator is a basic unit within Phantoscope. 

The Phantoscope project can complete different tasks because of the diversity of the operators it has.

You can follow our instructions to implement your own operator and add it to your Phantoscope project. 

Depending on its function, an operator can be classified into two types: processor and encoder. 

## Processor
Processors take up a larger portions of the operators in an application. A processor only processes the data that it is fed. When it is done, the pipeline takes its output to the next operator down the line. 

Generally speaking, the input to a processor has the same format as its output. For example, a processor takes in an image, extracts human face from it, and then send out the extracted inforamtion. 

## Encoder
An encoder is the last link in the pipeline. You can take an encoder as a special processor. The difference between an encoder and a processor includes: 

An encoder converts unstructured data to vectors or tags, so the input to an encoder is in a different format from its output.

# Design Principles of an Operator
An operator is stateless. 

An operator should be standalone and reusable. 

An operator is self-dependent and does not require an external storage. 
