{ pkgs ? import <nixpkgs> {} }:
with pkgs;

let
  python-packages = (python3.withPackages(ps: with ps; [
    selenium
    tabulate
  ]));
in
stdenv.mkDerivation rec {
  name = "autoqbid";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = [ python-packages geckodriver ];
}
