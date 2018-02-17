# Mode Inference

A prototype Python package for inferring datatypes and converting them into a relational schema. Written in pure Python.

| License | Release | Build Status | Codecov |
| :---: | :---: | :---: | :---: |
| [![][license img]][license] | [![][release img]][release] | [![Build Status](https://travis-ci.org/batflyer/Mode-Inference.svg?branch=master)](https://travis-ci.org/batflyer/Mode-Inference) | [![][codecov img]][codecov link] |

## Getting Started

**Prerequisites**

* Python (2.7, 3.3, 3.4, 3.5, 3.6)
  * `collections`, `argparse`, `re`: these should usually be installed already.
  
**Installation**

```
git clone https://github.com/batflyer/Mode-Inference.git
```

**Quick-Start Guide**

After you clone the repository:

```
cd Mode-Inference

# Create a directory for your datasets.
mkdir datasets

# Download one of the datasets from GitHub
curl -L https://github.com/boost-starai/BoostSRL-Misc/blob/master/Datasets/Toy-Cancer/Toy-Cancer.zip?raw=true > datasets/Toy-Cancer.zip

curl -L https://github.com/boost-starai/BoostSRL-Misc/blob/master/Datasets/Toy-Father/Toy-Father.zip?raw=true > datasets/Toy-Father.zip

# Unzip the Data
cd datasets
unzip Toy-Father.zip

# Infer modes:
python inferModes.py -pos datasets/Father/train/train_pos.txt -neg datasets/Father/train/train_neg.txt -fac datasets/Father/train/train_facts.txt
```

## Contributing

This software is in the early alpha stage: some features may simply not work, others may *work* but produce unexpected results. Nevertheless: suggestions, issues, general feedback, and pull requests are all welcome.

## Versioning

We use [SemVer](http://semver.org/) for versioning. See [Releases](https://github.com/batflyer/Mode-Inference/releases) for all stable versions that are available.

## License

    BSD 2-Clause License
    
    Copyright (c) 2018, Alexander L. Hayes
    All rights reserved.
    
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
    
    * Redistributions of source code must retain the above copyright notice, this
      list of conditions and the following disclaimer.
    
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Acknowledgements

* Professor Sriraam Natarajan
* Members of the STARAI Lab

[license]:LICENSE
[license img]:https://img.shields.io/github/license/batflyer/Mode-Inference.svg

[release]:https://github.com/batflyer/Mode-Inference/releases
[release img]:https://img.shields.io/github/tag/batflyer/Mode-Inference.svg

[codecov img]:https://codecov.io/gh/batflyer/Mode-Inference/branch/master/graphs/badge.svg?branch=master
[codecov link]:https://codecov.io/gh/batflyer/Mode-Inference?branch=master
