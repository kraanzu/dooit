{
  description = "Flake for Dooit";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        name = "dooit";
        version = "3.0.0";

        pkgs = import nixpkgs {inherit system;};
        python3 = pkgs.python312Packages;

        mainPkgs = with python3; [
          poetry-core
          pyperclip
          textual
          pyyaml
          dateutil
          sqlalchemy
          platformdirs
          tzlocal
        ];
      in {
        packages.default = python3.buildPythonPackage {
          pname = name;
          version = version;
          src = ./.;
          format = "pyproject";

          nativeBuildInputs = with pkgs; [
            poetry
          ];

          pythonRelaxDeps = [
            "textual"
            "tzlocal"
            "platformdirs"
          ];

          buildInputs = mainPkgs;

          # TODO: enable this
          doCheck = false; 
        };

        # Deps: Devshell
        devShell = pkgs.mkShell {
          buildInputs =
            mainPkgs
            ++ (with python3; [
              textual-dev
              mkdocs
              mkdocs-material
              pre-commit-hooks
              pytest
              pytest-aio
            ]);
        };
      }
    );
}
