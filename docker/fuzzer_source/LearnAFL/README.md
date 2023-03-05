# LearnAFL

## Introduction

LearnAFL is a knowledge-learn evolutionary fuzzer based on AFL(American Fuzzy Lop) and is written and maintained by Tai Yue \<yuetaisteinsgate@gmail.com\> or \<yuetai17@nudt.edu.cn\>. LearnAFL does not require any prior knowledge of the application or input format. It can learn partial knowledge of some paths by analyzing the test cases that exercise the paths. 

## Published Work

[LearnAFL: Greybox Fuzzing with Knowledge Enhancement](https://ieeexplore.ieee.org/document/8811487), IEEE Access

## Requirements

LearnAFL requires **python 2.7** to call the python script to learn knowledge. Other requirements are as same as those of AFL.

## How to install and run

The steps of installing and running LearnAFL are also as same as those of AFL. In addition, we complement the function of controlling the runtime. You can assign the runtime hours by adding the parameter `-e XXX` in running the afl-fuzz.
