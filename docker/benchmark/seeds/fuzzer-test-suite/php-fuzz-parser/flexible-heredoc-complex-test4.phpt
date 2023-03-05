<?php

{
    $FOO = "FOO";
    define("FOO", "FOO");
    $b = <<<FOO
    Test
    ${
        FOO
    }
    FOO;
    var_dump($b);
}

{
    $FOO = "FOO";
    $b = <<<FOO
        Test
        ${
        FOO
        }
    FOO;
    var_dump($b);
}

?>