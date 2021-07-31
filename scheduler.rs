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
        let mut freq: [i32; 29] = [0; 29];


        let mut i: isize = 0;

        while i < c_p_num as isize{

            freq[*c_p_course_id.offset(i as isize) as usize] += 1;

            i = i + 1;
        }


        *c_c_num = 0;
        let class_id_offset: i32 = 1000;

        let mut course_index = 0;
        for x in &freq{
            println!("Index: {}, Freq: {} ",course_index, x);

            let num_classes = (x+16)/15;

            println!("Number of classes for index: {}",num_classes);

            let mut i = 0;
            while i < num_classes+1 {
                *c_c_id.offset(*c_c_num as isize) = (*c_c_num)+class_id_offset;
                *c_c_course_id.offset(*c_c_num as isize) = course_index;
                *c_c_period.offset(*c_c_num as isize) = (i % 7) + 1;

                *c_c_num += 1;
                i += 1;
            }

            course_index += 1;
        }


        println!("Number of classes: {}",*c_c_num);


    }

}

/*
pub fn student_available(id: i32,period: i32,c_s_student_id: *mut i32, c_s_period: *mut i32) -> bool {
    unsafe {
        let mut i = 0;

        while i < 7000 {
            if *c_s_student_id.offset(i as isize) == id {
                if *c_s_period.offset(i as isize) == period {
                    return false;
                }
            }
            i += 1;
        }

        return true;
    }
}

pub fn course_available(course_id: i32, period: i32, c_c_course_id: *mut i32,c_c_period: *mut i32) -> bool {
    unsafe{
        let mut vec = Vec::new();

        let mut i = 0;
        while (i < 7000) {
            if *c_c_period.offset(i) == period {
                vec.push(i);
                return false;
            }
        }
        return true;
    }
}
 */