<?php

class Test {
    public static int $a;
    protected static int $b;
    private static int $c;

    static function run() {
        try {
            self::$a;
        } catch (Error $e) {
            echo $e->getMessage(), "\n";
        }
        try {
            self::$b;
        } catch (Error $e) {
            echo $e->getMessage(), "\n";
        }
        try {
            self::$c;
        } catch (Error $e) {
            echo $e->getMessage(), "\n";
        }
    }
}

Test::run();

?>