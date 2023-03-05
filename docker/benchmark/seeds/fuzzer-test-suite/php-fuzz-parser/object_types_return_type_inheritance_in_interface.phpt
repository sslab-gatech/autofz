<?php

interface One {
    public function a();
}

interface Two extends One {
    public function a() : object;
}

$three = new class implements Two {
    public function a() : object {
        return 12345;
    }
};
$three->a();