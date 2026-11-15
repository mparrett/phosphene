# Decode, onsets, live input over TCP and HTTP, and one headless frame per engine.
test:
    lg -source-paths src:test test/run.lg

# Rewrite the reference frames after an intended visual change.
update-refs:
    PHOSPHENE_UPDATE_REF=1 lg -source-paths src:test test/run.lg

# A native binary at out/phosphene through `lg compile`, which needs Go and an
# lg with the subcommand (let-go main until v1.14.0; 1.13.0 has none). Every
# namespace is passed so the render kernels lower too, not just the entry.
build lg="lg":
    #!/bin/sh
    set -e
    # lg compile resolves namespaces from the cwd, so it runs in src/; make a
    # path to lg absolute first, so a relative one still works from there.
    case "{{lg}}" in
      */*) lg="$(cd "$(dirname "{{lg}}")" && pwd)/$(basename "{{lg}}")" ;;
      *)   lg="{{lg}}" ;;
    esac
    mkdir -p out
    cd src
    "$lg" compile -o ../out/phosphene phosphene/cli.lg $(find phosphene -name '*.lg' ! -name cli.lg | sort)
