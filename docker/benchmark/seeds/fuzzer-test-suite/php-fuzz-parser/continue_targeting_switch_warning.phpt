<?php

function test() {
    switch ($foo) {
        case 0:
            continue; // INVALID
        case 1:
            break;
    }

    while ($foo) {
        switch ($bar) {
            case 0:
                continue; // INVALID
            case 1:
                continue 2;
            case 2:
                break;
        }
    }

    while ($foo) {
        switch ($bar) {
            case 0:
                while ($xyz) {
                    continue 2; // INVALID
                }
            case 1:
                while ($xyz) {
                    continue 3;
                }
            case 2:
                while ($xyz) {
                    break 2;
                }
        }
    }
}

?>