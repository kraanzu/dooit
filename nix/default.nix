{
  lib,
  fetchFromGitHub,
  dooit,
  python311,
  testers,
  nix-update-script,
  extraPackages ? [],
}: let
  python3 = python311;
  username = "dooit-org";
  repo = "dooit";
  ver = "v3.0.2";
in
  python3.pkgs.buildPythonApplication rec {
    pname = repo;
    version = ver;
    pyproject = true;

    src = fetchFromGitHub {
      owner = username;
      repo = pname;
      rev = ver;
      hash = "sha256-DPmCADFduGc5n+6q9zl0f4x9C6RmzLvBeYh2j0ZSpH0=";
    };

    build-system = with python3.pkgs; [poetry-core];

    pythonRelaxDeps = [
      "tzlocal"
      "textual"
      "sqlalchemy"
    ];

    propagatedBuildInputs = with python3.pkgs;
      [
        pyperclip
        textual
        pyyaml
        dateutil
        sqlalchemy
        platformdirs
        tzlocal
        click
      ]
      ++ extraPackages;

    # testing

    preBuild = ''
      export HOME=$(mktemp -d)
    '';

    nativeCheckInputs = with python3.pkgs; [pytest faker];
    doCheck = true;
    checkPhase = ''
      python -m pytest
    '';

    passthru = {
      tests.version = testers.testVersion {
        package = dooit;
        command = "HOME=$(mktemp -d) dooit --version";
      };

      updateScript = nix-update-script {};
    };

    meta = with lib; {
      description = "TUI todo manager";
      homepage = "https://github.com/${username}/${pname}";
      changelog = "https://github.com/${username}/${pname}/blob/v${ver}/CHANGELOG.md";
      license = licenses.mit;
      maintainers = with maintainers; [
        khaneliman
        wesleyjrz
        kraanzu
      ];
      mainProgram = "dooit";
    };
  }
