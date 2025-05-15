{ pkgs }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.python312Packages.setuptools
    pkgs.python312Packages.wheel

    pkgs.opencv
    pkgs.libGL

    pkgs.tesseract
  ];
}
