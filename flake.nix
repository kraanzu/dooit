{
  description = "Flake for Dooit with default.nix integration";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
    ...
  }: let
    forEachSystem = nixpkgs.lib.genAttrs nixpkgs.lib.platforms.all;

    pkgsFor = forEachSystem (
      system:
        import nixpkgs {
          inherit system;
        }
    );

    packageFor = system: extraPackages:
      pkgsFor.${system}.callPackage ./nix {
        inherit extraPackages;
      };
  in {
    packages = forEachSystem (
      system: {
        default = packageFor system [];
      }
    );

    overlay = final: prev: {
      dooit = extraPackages: packageFor final.system extraPackages;
    };
  };
}
