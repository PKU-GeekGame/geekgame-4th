pub(super) trait WithLen {
    fn len(&self) -> usize;
}

pub(super) unsafe trait CanGet: WithLen + Send + Sync {
    fn data(&self) -> *const u8;

    unsafe fn get_unchecked(&self, index: usize) -> u8 {
        self.data().add(index).read()
    }

    fn try_get(&self, index: usize) -> Option<u8> {
        if index < self.len() {
            Some(unsafe { self.get_unchecked(index) })
        } else {
            None
        }
    }

    fn get(&self, index: usize) -> u8 {
        assert!(index < self.len());
        unsafe { self.get_unchecked(index) }
    }
}

pub(super) unsafe trait CanPut: WithLen + Send + Sync {
    fn data_mut(&mut self) -> *mut u8;

    fn put(&mut self, index: usize, data: u8) -> u8 {
        assert!(index < self.len());
        unsafe { self.put_unchecked(index, data) }
    }

    fn try_put(&mut self, index: usize, data: u8) -> Option<u8> {
        if index < self.len() {
            Some(unsafe { self.put_unchecked(index, data) })
        } else {
            None
        }
    }

    unsafe fn put_unchecked(&mut self, index: usize, data: u8) -> u8 {
        self.data_mut().add(index).replace(data)
    }
}

pub(super) trait CanBoth: Send + Sync + CanPut + CanGet {}
