{
  description = "Flake for Dooit";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }
  :
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
          click
        ];
      in {
        packages.default = {extraPackages ? []}:
          python3.buildPythonPackage {
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

            buildInputs = mainPkgs ++ extraPackages;
            propagatedBuildInputs = mainPkgs;

            # TODO: enable this
            doCheck = false;
          };

        # Deps: Devshell
        devShell = pkgs.mkShell {
          name = "dooit";
          buildInputs =
            mainPkgs
            ++ (with python3; [
              textual-dev
              pre-commit-hooks
              pytest
              pytest-aio
              faker
            ])
            ++ [pkgs.bun];
          shellHook = ''
            cd site/
            ${pkgs.bun}/bin/bun install
            cd ..
          '';
        };
      }
    );
}
