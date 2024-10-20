#![feature(cell_leak)]
#![feature(slice_ptr_get)]
#![feature(trait_upcasting)]
#![feature(try_blocks)]

use std::{
    cell::{self, RefCell},
    fs::File,
    marker::PhantomData,
    mem::ManuallyDrop,
    ptr::NonNull,
    sync::RwLock,
};

use impls::{BoxedData, RawData};
use traits::{CanBoth, CanGet, CanPut};

mod impls;
mod traits;

enum Data {
    ReadOnly(Box<dyn CanGet>),
    WriteOnly(Box<dyn CanPut>),
    ReadWrite(Box<dyn CanBoth>),
}

impl Data {
    fn read(&self) -> Option<&dyn CanGet> {
        match self {
            Self::ReadOnly(val) => Some(val.as_ref()),
            Self::WriteOnly(_) => None,
            Self::ReadWrite(val) => Some(val.as_ref() as _),
        }
    }

    fn write(&mut self) -> Option<&mut dyn CanPut> {
        match self {
            Self::ReadOnly(_) => None,
            Self::WriteOnly(val) => Some(val.as_mut()),
            Self::ReadWrite(val) => Some(val.as_mut() as _),
        }
    }
}

static GLOBAL_DATA: RwLock<[u8; 1024]> = RwLock::new([0; 1024]);

struct App<'a> {
    data: Vec<Data>,
    is_admin: bool,
    _marker: PhantomData<&'a RefCell<[u8; 1024]>>,
}

macro_rules! read {
    ($prompt:literal) => {{
        println!($prompt);
        text_io::read!()
    }};
}

impl<'a> App<'a> {
    fn process(&mut self, local_data: &'a RefCell<[u8; 1024]>) {
        let choice: u32 = read!(
            "Please choose:\n\
            1. Create\n\
            2. Read\n\
            3. Write\n\
            Enter the choice:"
        );

        match choice {
            1 => self.create(local_data),
            2 => self.read(),
            3 => self.write(),
            _ => println!("Bad choice!"),
        }
    }

    fn create(&mut self, local_data: &'a RefCell<[u8; 1024]>) {
        let choice: u32 = read!(
            "Please choose:\n\
            1. Boxed\n\
            2. Global\n\
            3. Local\n\
            Enter the choice:"
        );
        if !(1..=3).contains(&choice) {
            println!("Bad choice");
            return;
        }

        let size: usize = read!("Enter the size:");
        if size > 4096 {
            println!("Too large!");
            return;
        } else if choice != 1 && size != 1024 {
            println!("Not supported!");
            return;
        }

        let perm: u32 = read!(
            "Please choice\n\
            1. Read only\n\
            2. Write only\n\
            3. Read write\n\
            Enter the choice:"
        );

        let data: Option<_> = try {
            match (choice, perm) {
                (1, 1) => Data::ReadOnly(Box::new(BoxedData::new(size)) as _),
                (1, 2) => Data::WriteOnly(Box::new(BoxedData::new(size)) as _),
                (1, 3) => Data::ReadWrite(Box::new(BoxedData::new(size)) as _),
                (2, 1) => unsafe {
                    Data::ReadOnly(Box::new(RawData::new(
                        NonNull::from(ManuallyDrop::new(GLOBAL_DATA.try_read().ok()?).as_ref())
                            .as_non_null_ptr(),
                        1024,
                    )))
                },
                (2, 2) => unsafe {
                    Data::WriteOnly(Box::new(RawData::new(
                        NonNull::from(ManuallyDrop::new(GLOBAL_DATA.try_write().ok()?).as_ref())
                            .as_non_null_ptr(),
                        1024,
                    )))
                },
                (2, 3) => unsafe {
                    Data::ReadWrite(Box::new(RawData::new(
                        NonNull::from(ManuallyDrop::new(GLOBAL_DATA.try_write().ok()?).as_ref())
                            .as_non_null_ptr(),
                        1024,
                    )))
                },
                (3, 1) => unsafe {
                    Data::ReadOnly(Box::new(RawData::new(
                        NonNull::from(cell::Ref::leak(local_data.try_borrow().ok()?).as_ref())
                            .as_non_null_ptr(),
                        1024,
                    )))
                },
                (3, 2) => unsafe {
                    Data::WriteOnly(Box::new(RawData::new(
                        NonNull::from(
                            cell::RefMut::leak(local_data.try_borrow_mut().ok()?).as_mut(),
                        )
                        .as_non_null_ptr(),
                        1024,
                    )))
                },
                (3, 3) => unsafe {
                    Data::ReadWrite(Box::new(RawData::new(
                        NonNull::from(
                            cell::RefMut::leak(local_data.try_borrow_mut().ok()?).as_mut(),
                        )
                        .as_non_null_ptr(),
                        1024,
                    )))
                },
                _ => {
                    println!("Bad choice!");
                    return;
                }
            }
        };
        let Some(data) = data else {
            println!("Guard violation!");
            return;
        };

        println!("Slot: {}", self.data.len());
        self.data.push(data);
    }

    fn read(&self) {
        let slot: usize = read!("Enter the slot:");

        let read = match self.data.get(slot).map(|data| data.read()) {
            Some(Some(read)) => read,
            Some(None) => {
                println!("Read not allowed!");
                return;
            }
            None => {
                println!("Bad index!");
                return;
            }
        };

        let index: usize = read!("Enter the index:");

        let choice: u32 = read!(
            "Please choose:\n\
            1. Read (unwrap)\n\
            2. Read (try)\n\
            3. Read (unchecked)\n\
            Enter the choice:"
        );

        match choice {
            1 => println!("Result: {}", read.get(index)),
            2 => println!("Result: {:?}", read.try_get(index)),
            3 if self.is_admin || index < read.len() => {
                println!("Result: {}", unsafe { read.get_unchecked(index) });
            }
            3 => {
                println!("No privilege!");
            }
            _ => {
                println!("Bad choice!")
            }
        }
    }

    fn write(&mut self) {
        let slot: usize = read!("Enter the slot:");

        let write = match self.data.get_mut(slot).map(|data| data.write()) {
            Some(Some(write)) => write,
            Some(None) => {
                println!("Read not allowed!");
                return;
            }
            None => {
                println!("Bad index!");
                return;
            }
        };

        let index: usize = read!("Enter the index:");
        let value: u8 = read!("Enter the value:");

        let choice: u32 = read!(
            "Please choose:\n\
            1. Write (unwrap)\n\
            2. Write (try)\n\
            3. Write (unchecked)\n\
            Enter the choice:"
        );

        match choice {
            1 => println!("Result: {}", write.put(index, value)),
            2 => println!("Result: {:?}", write.try_put(index, value)),
            3 if self.is_admin || index < write.len() => {
                println!("Result: {}", unsafe { write.put_unchecked(index, value) });
            }
            3 => {
                println!("No privilege!");
            }
            _ => {
                println!("Bad choice!")
            }
        }
    }
}

fn main() {
    let local_data = RefCell::new([0; 1024]);

    let mut app = App {
        data: Vec::new(),
        is_admin: File::create("/root/check").is_ok(),
        _marker: PhantomData,
    };

    loop {
        app.process(&local_data);
    }
}
