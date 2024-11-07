{
  description = "Flake for Dooit";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = inputs: let
    # Define function to generate attributes for each system
    forEachSystem = inputs.nixpkgs.lib.genAttrs inputs.nixpkgs.lib.platforms.all;

    # Import nixpkgs for each system
    pkgsFor = forEachSystem (
      system:
        import inputs.nixpkgs {
          inherit system;
        }
    );

    # Common Python packages used in both main package and devShell
    mainPkgs = python3:
      with python3; [
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

    # Additional packages for the devShell
    devShellPkgs = python3:
      with python3; [
        textual-dev
        pre-commit-hooks
        pytest
        pytest-aio
        faker
      ];

    # Native build inputs
    nativeBuildInputs = pkgs:
      with pkgs; [
        poetry
      ];

    # Define devShell for each system
    devShellFor = system:
      inputs.nixpkgs.lib.genAttrs ["default"] (
        _:
          pkgsFor.${system}.mkShell {
            buildInputs =
              (mainPkgs pkgsFor.${system}.python312Packages)
              ++ (devShellPkgs pkgsFor.${system}.python312Packages)
              ++ [pkgsFor.${system}.bun];

            shellHook = ''
              cd site/
              ${pkgsFor.${system}.bun}/bin/bun install
              cd ..
            '';
          }
      );

    # Define default package for each system
    defaultPackageFor = system:
      pkgsFor.${system}.python312Packages.buildPythonPackage {
        pname = "dooit";
        version = "3.0.0";
        src = ./.;
        format = "pyproject";

        nativeBuildInputs = nativeBuildInputs pkgsFor.${system};

        pythonRelaxDeps = [
          "textual"
          "tzlocal"
          "platformdirs"
          "sqlalchemy"
        ];

        buildInputs = mainPkgs pkgsFor.${system}.python312Packages;
        propagatedBuildInputs = mainPkgs pkgsFor.${system}.python312Packages;

        doCheck = false;
      };
  in {
    # Define the devShells for each system
    devShells = forEachSystem devShellFor;

    # Define the default package for each system
    packages = forEachSystem (
      system: {
        default = defaultPackageFor system;
      }
    );

    # Expose a top-level `defaultPackage` that detects the current system
    defaultPackage = defaultPackageFor inputs.nixpkgs.lib.systems.defaultSystem;
  };
}
