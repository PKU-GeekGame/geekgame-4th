use std::ptr::NonNull;

use crate::traits::{CanBoth, CanGet, CanPut, WithLen};

pub(super) struct BoxedData {
    data: Box<[u8]>,
}

impl BoxedData {
    pub(super) fn new(len: usize) -> Self {
        Self {
            data: vec![0; len].into_boxed_slice(),
        }
    }
}

impl WithLen for BoxedData {
    fn len(&self) -> usize {
        self.data.len()
    }
}

unsafe impl CanGet for BoxedData {
    fn data(&self) -> *const u8 {
        self.data.as_ptr()
    }
}

unsafe impl CanPut for BoxedData {
    fn data_mut(&mut self) -> *mut u8 {
        self.data.as_mut_ptr()
    }
}

impl CanBoth for BoxedData {}

pub(super) struct RawData {
    ptr: NonNull<u8>,
    len: usize,
}

unsafe impl Send for RawData {}
unsafe impl Sync for RawData {}

impl RawData {
    pub(super) unsafe fn new(ptr: NonNull<u8>, len: usize) -> Self {
        Self { ptr, len }
    }
}

impl WithLen for RawData {
    fn len(&self) -> usize {
        self.len
    }
}

unsafe impl CanGet for RawData {
    fn data(&self) -> *const u8 {
        self.ptr.as_ptr().cast_const()
    }
}

unsafe impl CanPut for RawData {
    fn data_mut(&mut self) -> *mut u8 {
        self.ptr.as_ptr()
    }
}

impl CanBoth for RawData {}
