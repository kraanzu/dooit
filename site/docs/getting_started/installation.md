# Installing Dooit & Dooit Extras

Dooit can be installed via various package managers

## PyPI

```bash
pip install dooit dooit-extras
```

## Arch Linux

```bash
yay -S dooit-bin dooit-extras
```

## NixOS

### Flakes :snowflake:

```nix{25,7-8,}
# flake.nix

{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable"; # this can be stable, but if it is do not make hyprpanel follow it

    dooit.url = "github:kraanzu/dooit/develop";
    dooit-extras.url = "github:dooit-org/dooit-extras";
  };
  # ...

  outputs = inputs @ {
    nixpkgs,
    ...
  }: let
    pkgs = import nixpkgs {};
    system = "x86_64-linux"; # change to whatever your system should be
  in {
    nixosConfigurations."${host}" = nixpkgs.lib.nixosSystem {
      specialArgs = {
        inherit system inputs pkgs;
      };
      modules = [
        # ...
        ./dooit.nix
      ];
    };
  };
}
```

```nix
# dooit.nix

{
  inputs,
  pkgs,
  ...
}: let
  mydooit = pkgs.dooit.override {
    extraPackages = [
      pkgs.dooit-extras
    ];
  };
in {

  # this overlay allows you to use dooit from pkgs.dooit
  nixpkgs.overlays = [inputs.dooit.overlay inputs.dooit-extras.overlay];

  environment.systemPackages = [
    mydooit
  ];
}
```

> Thanks to [`Hyprpanel`](https://hyprpanel.com/) from whom I stole the format for the flake
