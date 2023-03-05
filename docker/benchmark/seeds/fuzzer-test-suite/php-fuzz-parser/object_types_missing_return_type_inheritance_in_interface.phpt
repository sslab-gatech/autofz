<?php

interface One {
    public function a() : object;
}

interface Two extends One {
    public function a();
}