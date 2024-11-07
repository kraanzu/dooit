{
  lib,
  fetchFromGitHub,
  dooit,
  python311,
  testers,
  nix-update-script,
}: let
  python3 = python311;
in
  python3.pkgs.buildPythonApplication rec {
    pname = "dooit";
    version = "3.0.0";
    pyproject = true;

    src = fetchFromGitHub {
      owner = "kraanzu";
      repo = "dooit";
      rev = "develop"; # TODO: Change to version
      hash = "sha256-N0r37iEj0P/qLBFG9bGPUPjw31Wk9kA+rrZd59Yrxd4=";
    };

    build-system = with python3.pkgs; [poetry-core];

    pythonRelaxDeps = [
      "tzlocal"
      "textual"
    ];

    propagatedBuildInputs = with python3.pkgs; [
      pyperclip
      textual
      pyyaml
      dateutil
      sqlalchemy
      platformdirs
      tzlocal
      click
    ];

    # No tests available
    doCheck = true;

    passthru = {
      tests.version = testers.testVersion {
        package = dooit;
        command = "HOME=$(mktemp -d) dooit --version";
      };

      updateScript = nix-update-script {};
    };

    meta = with lib; {
      description = "TUI todo manager";
      homepage = "https://github.com/kraanzu/dooit";
      changelog = "https://github.com/kraanzu/dooit/blob/develop/CHANGELOG.md"; # TODO: change to version
      license = licenses.mit;
      maintainers = with maintainers; [
        khaneliman
        wesleyjrz
        kraanzu
      ];
      mainProgram = "dooit";
    };
  }
