{
  description = "env";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        nixFormatter = pkgs.nixfmt-rfc-style;
        defaultPkgs = [
          nixFormatter
          pkgs.ruff
        ];
        mkDevShell =
          {
            extraPkgs ? [ ],
            shellHook ? "",
            name ? "dev",
          }:
          pkgs.mkShell {
            name = name;
            packages = defaultPkgs ++ extraPkgs;
            shellHook = shellHook;
          };
      in
      {
        formatter = nixFormatter;

        devShells = {
          default = mkDevShell {
            name = "default";
            extraPkgs = [
              pkgs.uv
              pkgs.python312
              pkgs.beamMinimal28Packages.elixir_1_19
              pkgs.livebook
              pkgs.swi-prolog
            ];
          };
        };
      }
    );
}
