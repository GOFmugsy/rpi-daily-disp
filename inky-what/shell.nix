with import <nixpkgs> {};
let
  pythonEnv = python3.withPackages (ps: [
    ps.numpy
    ps.toolz
    ps.pillow
    ps.pip
  ]);

  smbus2 = pkgs.python38Packages.buildPythonPackage rec {
    pname = "smbus2";
    version = "0.4.1";
 
    src = pkgs.python38Packages.fetchPypi {
      inherit pname version;
      sha256 = "6276eb599b76c4e74372f2582d2282f03b4398f0da16bc996608e4f21557ca9b";
    };

    propagatedBuildInputs = with pkgs.python38Packages; [ h2 multidict ];

    doCheck = false;
  };

  inky = pkgs.python38Packages.buildPythonPackage rec {
    pname = "inky";
    version = "1.2.2";

    src = pkgs.python38Packages.fetchPypi {
      inherit pname version;
      sha256 = "5eeee0a35314f76af3a614805db0227952aaa22d062f280eafe7d0ae40a01cce";
    };

    propagatedBuildInputs = with pkgs.python38Packages; [ h2 multidict spidev numpy pillow smbus2 ];

    doCheck = false;
  };

  customPython = pkgs.python38.buildEnv.override {
    # extraLibs = [ spidev inky ];
    extraLibs = [ inky ];
  };
in mkShell {
  buildInputs = [
    pkgs.python38
    customPython
  ];
  packages = [
    python3
    pythonEnv
    black
    mypy
    libffi
    openssl
  ];
}

