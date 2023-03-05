<?php

interface One {
    public function a() : object;
}

class Two implements One {
    public function a() : object {}
}

function a() : object {}

$returnTypeOne = (new ReflectionClass(One::class))->getMethod('a')->getReturnType();
var_dump($returnTypeOne->isBuiltin(), $returnTypeOne->getName());

$returnTypeTwo = (new ReflectionClass(Two::class))->getMethod('a')->getReturnType();
var_dump($returnTypeTwo->isBuiltin(), $returnTypeTwo->getName());

$returnTypea = (new ReflectionFunction('a'))->getReturnType();
var_dump($returnTypea->isBuiltin(), $returnTypea->getName());