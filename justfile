# Decode, onsets, live input over TCP, and one headless frame per engine.
test:
    lg -source-paths src:test test/run.lg

# Rewrite the reference frames after an intended visual change.
update-refs:
    PHOSPHENE_UPDATE_REF=1 lg -source-paths src:test test/run.lg
