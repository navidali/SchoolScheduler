#[no_mangle]

pub fn schedule(c_p_course_id: *const i32,
                c_p_student_id: *const i32,
                c_p_period: *const i32,
                c_p_num: usize,

                c_c_id: *mut i32,
                c_c_course_id: *mut i32,
                c_c_period: *mut i32,
                c_c_num: *mut i32,

                c_s_student_id: *mut i32,
                c_s_class_id: *mut i32,
                c_s_period: *mut i32,
                c_s_num: *mut i32){
    unsafe{
        let mut freq: Vec<i32> = Vec::new();


        let mut i: isize = 0;

        while i < c_p_num as isize{

            //freq[*c_p_course_id.offset(i as isize) as usize] += 1;
            println!("Hello");
            i = i + 1;
        }


        *c_s_num = 101;
    }

}