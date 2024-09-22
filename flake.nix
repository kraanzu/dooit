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
        devShell = pkgs.mkShell {
          buildInputs = with pkgs.python312Packages; [
            # main
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
