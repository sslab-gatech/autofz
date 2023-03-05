<?php

$binops = [
    '+',
    '-',
    '*',
    '/',
    '%',
    '**',
    '<<',
    '>>',
    '&',
    '|',
    '^',
    // Works on booleans, never errors.
    'xor',
    // Only generates errors that string conversion emits.
    '.',
];
$illegalValues = [
    '[]',
    'new stdClass',
    'STDOUT',
];
$legalValues = [
    'null',
    'true',
    'false',
    '2',
    '3.5',
    '"123"',
    '"foo"', // Semi-legal.
];

set_error_handler(function($errno, $errstr) {
    assert($errno == E_WARNING);
    echo "Warning: $errstr\n";
});

function evalBinOp(string $op, string $value1, string $value2) {
    try {
        eval("return $value1 $op $value2;");
        echo "No error for $value1 $op $value2\n";
    } catch (Throwable $e) {
        echo $e->getMessage() . "\n";
    }
}

function evalAssignOp(string $op, string $value1, string $value2) {
    $x = $origX = eval("return $value1;");
    try {
        eval("\$x $op= $value2;");
        echo "No error for $value1 $op= $value2\n";
    } catch (Throwable $e) {
        echo $e->getMessage() . "\n";
        if ($x !== $origX) {
            die("Value corrupted!");
        }
    }
}

echo "BINARY OP:\n";
foreach ($binops as $op) {
    foreach ($illegalValues as $illegalValue1) {
        foreach ($illegalValues as $illegalValue2) {
            evalBinOp($op, $illegalValue1, $illegalValue2);
        }
    }
    foreach ($illegalValues as $illegalValue) {
        foreach ($legalValues as $legalValue) {
            evalBinOp($op, $illegalValue, $legalValue);
            evalBinOp($op, $legalValue, $illegalValue);
        }
    }
}

echo "\n\nASSIGN OP:\n";
foreach ($binops as $op) {
    if ($op === 'xor') continue;

    foreach ($illegalValues as $illegalValue1) {
        foreach ($illegalValues as $illegalValue2) {
            evalAssignOp($op, $illegalValue1, $illegalValue2);
        }
    }
    foreach ($illegalValues as $illegalValue) {
        foreach ($legalValues as $legalValue) {
            evalAssignOp($op, $illegalValue, $legalValue);
            evalAssignOp($op, $legalValue, $illegalValue);
        }
    }
}

echo "\n\nUNARY OP:\n";
foreach ($illegalValues as $illegalValue) {
    try {
        eval("return ~$illegalValue;");
        echo "No error for ~$copy\n";
    } catch (TypeError $e) {
        echo $e->getMessage() . "\n";
    }
}

echo "\n\nINCDEC:\n";
foreach ($illegalValues as $illegalValue) {
    $copy = eval("return $illegalValue;");
    try {
        $copy++;
        echo "No error for $copy++\n";
    } catch (TypeError $e) {
        echo $e->getMessage() . "\n";
    }
    $copy = eval("return $illegalValue;");
    try {
        $copy--;
        echo "No error for $copy--\n";
    } catch (TypeError $e) {
        echo $e->getMessage() . "\n";
    }
}

?>