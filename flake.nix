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
        pkgs = import nixpkgs {inherit system;};
      in {
        packages.default = pkgs.python312Packages.buildPythonPackage {
          pname = "dooit";
          version = "3.0.0";

          src = ./.;

          format = "pyproject";

          nativeBuildInputs = with pkgs; [
            poetry # For managing pyproject.toml dependencies
          ];

          pythonRelaxDeps = [
            "textual"
            "tzlocal"
            "platformdirs"
          ];

          buildInputs = with pkgs.python312Packages; [
            poetry-core
            pyperclip
            textual
            pyyaml
            dateutil
            sqlalchemy
            platformdirs
            tzlocal
          ];
        };

        # Optional devShell for development
        devShell = pkgs.mkShell {
          buildInputs = with pkgs.python312Packages; [
            poetry-core
            pyperclip
            textual
            pyyaml
            dateutil
            sqlalchemy
            platformdirs

            # dev
            textual-dev
            mkdocs
            mkdocs-material
            pre-commit-hooks
            pytest
            pytest-aio
          ];
        };
      }
    );
}
