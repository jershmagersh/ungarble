# Ungarble

This project uses the Binary Ninja disassembly API to find strings that have been obfuscated using the [garble](https://github.com/burrowers/garble) project and emulates their obfuscation routines to recover the original strings. This is very much in the experimental stage, and this example uses a single sample to accomplish this.

## Architecture

The [Dockerfile](Dockerfile) will create a container to serve as our emulation interface. This is in order to avoid emulating (potentially) malicious instructions on our host machine (I understand that Docker is not considered a security boundary). This will construct a Docker image containing [https://github.com/binref/refinery](https://github.com/binref/refinery), its required dependencies and the samples within the `samples` directory.

## Obfuscated String Identification

Identifying strings obfuscated with garble proved to be more challenging than I initially thought. The obfuscation routines contain a set of standardized operations, however, these are fairly difficult to fingerprint due to the Golang compiler output. I attempted to use intermediate languages within Binary Ninja, however, this proved to be unreliable either due to the set of operations being too large (and therefore hitting decompiler limits and the function not decompiling), non-stand patterns being identified, fingerprinting taking too long, etc.

## Emulation 

The [https://binref.github.io/units/formats/exe/vstack.html](https://binref.github.io/units/formats/exe/vstack.html) unit is used within this experimental stage as it allows rapid prototyping torecover strings from stack writes using emulation with Unicorn. This is implemented in the [scripts/vstack.sh](scripts/vstack.sh) that is called within our container once start and end emulation addresses have been identified.
