{
  description = "Flake for Dooit";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = inputs: let
    forEachSystem = inputs.nixpkgs.lib.genAttrs inputs.nixpkgs.lib.platforms.all;

    pkgsFor = forEachSystem (
      system:
        import inputs.nixpkgs {
          inherit system;
        }
    );

    mainPkgs = python3: with python3; [
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

    devShellPkgs = python3: with python3; [
      textual-dev
      pre-commit-hooks
      pytest
      pytest-aio
      faker
    ];

    nativeBuildInputs = pkgs: with pkgs; [
      poetry
    ];

    # Define devShell for each system
    devShellFor = system:
      inputs.nixpkgs.lib.genAttrs ["default"] (
        _:
          pkgsFor.${system}.mkShell {
            buildInputs = (mainPkgs pkgsFor.${system}.python312Packages)
              ++ (devShellPkgs pkgsFor.${system}.python312Packages)
              ++ [ pkgsFor.${system}.bun ];

            shellHook = ''
              cd site/
              ${pkgsFor.${system}.bun}/bin/bun install
              cd ..
            '';
          }
      );

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
    devShells = forEachSystem devShellFor;
    packages = forEachSystem (
      system: {
        default = defaultPackageFor system;
      }
    );
  };
}
