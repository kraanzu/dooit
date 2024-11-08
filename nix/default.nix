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
  # ver = "3.0.0";
  ver = "main"; # TODO: Change to version
in
  python3.pkgs.buildPythonApplication rec {
    pname = repo;
    version = ver;
    pyproject = true;

    src = fetchFromGitHub {
      owner = username;
      repo = pname;
      rev = ver;
      hash = "sha256-U1C1Ht6sNh1skjukGKeCcOxYMplsJ+XCWH/Pa4ylZZc=";
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
      homepage = "https://github.com/${username}/${pname}";
      changelog = "https://github.com/${username}/${pname}/blob/${ver}/CHANGELOG.md";
      license = licenses.mit;
      maintainers = with maintainers; [
        khaneliman
        wesleyjrz
        kraanzu
      ];
      mainProgram = "dooit";
    };
  }
