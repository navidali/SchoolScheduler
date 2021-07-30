#[no_mangle]

pub fn schedule(c_p_course_id: *const i32 ,c_s_num: *mut i32){
    unsafe{
        *c_s_num = 100;
        println!("Hello")
    }

}