#!/usr/bin/env bash

state=$1

mongo rumba <<EOF
db.mic_state.update(
    { },
    {state: "$state" },
    {upsert: true }
)
EOF
