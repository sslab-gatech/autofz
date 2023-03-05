<?php

interface One {
    public function a() : object;
}

class Two implements One {
    public function a() : object {}
}

$three = new class extends Two {
    public function a() : object {
        return 12345;
    }
};
$three->a();