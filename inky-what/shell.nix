with import <nixpkgs> {};
let
  pythonEnv = python3.withPackages (ps: [
    ps.numpy
    ps.toolz
    ps.pillow
    ps.pip
  ]);
in mkShell {
  packages = [
    pythonEnv

    black
    mypy

    libffi
    openssl
  ];
}

