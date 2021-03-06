with import <nixpkgs> {};
let

  fonts-i = pkgs.python38Packages.buildPythonPackage rec {
    pname = "font-intuitive";
    version = "0.0.4";
 
    src = pkgs.python38Packages.fetchPypi {
      inherit pname version;
      sha256 = "f5744edf796949252bf3c8feb29b4c685c3e76f7848be638d3a9512e4730ee80";
    };

    propagatedBuildInputs = with pkgs.python38Packages; [ h2 multidict ];

    doCheck = false;
  };

  fonts-hk = pkgs.python38Packages.buildPythonPackage rec {
    pname = "font-hanken-grotesk";
    version = "0.0.2";
 
    src = pkgs.python38Packages.fetchPypi {
      inherit pname version;
      sha256 = "3bb66ce05819ff8ccd563e039dec462912579b8290f143152459865740723f39";
    };

    propagatedBuildInputs = with pkgs.python38Packages; [ h2 multidict ];

    doCheck = false;
  };

  fonts = pkgs.python38Packages.buildPythonPackage rec {
    pname = "fonts";
    version = "0.0.3";
 
    src = pkgs.python38Packages.fetchPypi {
      inherit pname version;
      sha256 = "c626655b75a60715e118e44e270656fd22fd8f54252901ff6ebf1308ad01c405";
    };

    propagatedBuildInputs = with pkgs.python38Packages; [ h2 multidict fonts-hk fonts-i ];

    doCheck = false;
  };

  rpi.gpio = pkgs.python38Packages.buildPythonPackage rec {
    pname = "RPi.GPIO";
    version = "0.7.0";
 
    src = pkgs.python38Packages.fetchPypi {
      inherit pname version;
      sha256 = "7424bc6c205466764f30f666c18187a0824077daf20b295c42f08aea2cb87d3f";
    };

    propagatedBuildInputs = with pkgs.python38Packages; [ h2 multidict ];

    doCheck = false;
  };

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

    propagatedBuildInputs = with pkgs.python38Packages; [ h2 multidict spidev numpy pillow smbus2 rpi.gpio fonts setuptools ];

    doCheck = false;
  };

  customPython = pkgs.python38.buildEnv.override {
    extraLibs = [ inky fonts ];
  };
in mkShell {
  buildInputs = [
    pkgs.python38
    customPython
  ];
  packages = [
    black
    libffi
    openssl
  ];
}

