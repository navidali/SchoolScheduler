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
        let mut freq: [i32; 30] = [0; 30];


        let mut i: isize = 0;

        while i < c_p_num as isize{

            freq[*c_p_course_id.offset(i as isize) as usize] += 1;

            i = i + 1;
        }


        let class_id = 0;
        let offset: i32 = 1000;

        let mut course_index = 0;
        for x in &freq{
            println!("Index: {}, Freq: {} ",course_index, x);

            let num_classes = (x+16)/15;



            course_index += 1;
        }

        *c_s_num = 101;
    }

}