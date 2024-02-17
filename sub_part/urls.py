from django.urls import path, include
from sub_part import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("admission_enquiry", views.admission_enquiry, name="admission_enquiry"),
    path(
        "admission_enquiry_edit/<pk>",
        views.admission_enquiry_edit,
        name="admission_enquiry_edit",
    ),
    path(
        "admission_enquiry_view/<pk>",
        views.admission_enquiry_view,
        name="admission_enquiry_view",
    ),
    path(
        "admission_enquiry_delete/<pk>",
        views.admission_enquiry_delete,
        name="admission_enquiry_delete",
    ),
    path("visitor_book", views.visitor_book, name="visitor_book"),
    path("visitor_book_edit/<pk>", views.visitor_book_edit, name="visitor_book_edit"),
    path("visitor_book_view/<pk>", views.visitor_book_view, name="visitor_book_view"),
    path(
        "visitor_book_delete/<pk>",
        views.visitor_book_delete,
        name="visitor_book_delete",
    ),
    path("phone_call_log", views.phone_call_log, name="phone_call_log"),
    path(
        "phone_call_log_edit/<pk>",
        views.phone_call_log_edit,
        name="phone_call_log_edit",
    ),
    path(
        "phone_call_log_view/<pk>",
        views.phone_call_log_view,
        name="phone_call_log_view",
    ),
    path(
        "phone_call_log_delete/<pk>",
        views.phone_call_log_delete,
        name="phone_call_log_delete",
    ),
    path("postal_dispatch", views.postal_dispatch, name="postal_dispatch"),
    path(
        "postal_dispatch_edit/<pk>",
        views.postal_dispatch_edit,
        name="postal_dispatch_edit",
    ),
    path(
        "postal_dispatch_View/<pk>",
        views.postal_dispatch_view,
        name="postal_dispatch_view",
    ),
    path(
        "postal_dispatch_delete/<pk>",
        views.postal_dispatch_delete,
        name="postal_dispatch_delete",
    ),
    path("postal_receive", views.postal_receive, name="postal_receive"),
    path(
        "postal_receive_edit/<pk>",
        views.postal_receive_edit,
        name="postal_receive_edit",
    ),
    path(
        "postal_receive_view/<pk>",
        views.postal_receive_view,
        name="postal_receive_view",
    ),
    path(
        "postal_receive_delete/<pk>",
        views.postal_receive_delete,
        name="postal_receive_delete",
    ),
    path("complain", views.complain, name="complain"),
    path("complain_edit/<pk>", views.complain_edit, name="complain_edit"),
    path("complain_view/<pk>", views.complain_view, name="complain_view"),
    path("complain_delete/<pk>", views.complain_delete, name="complain_delete"),
    path(
        "setup_front_office_purpose",
        views.setup_front_office_purpose,
        name="setup_front_office_purpose",
    ),
    path(
        "setup_front_office_purpose_edit/<pk>",
        views.setup_front_office_purpose_edit,
        name="setup_front_office_purpose_edit",
    ),
    path(
        "setup_front_office_purpose_delete/<pk>",
        views.setup_front_office_purpose_delete,
        name="setup_front_office_purpose_delete",
    ),
    path(
        "setup_front_office_complain_type",
        views.setup_front_office_complain_type,
        name="setup_front_office_complain_type",
    ),
    path(
        "setup_front_office_complain_type_edit/<pk>",
        views.setup_front_office_complain_type_edit,
        name="setup_front_office_complain_type_edit",
    ),
    path(
        "setup_front_office_complain_type_delete/<pk>",
        views.setup_front_office_complain_type_delete,
        name="setup_front_office_complain_type_delete",
    ),
    path(
        "setup_front_office_source",
        views.setup_front_office_source,
        name="setup_front_office_source",
    ),
    path(
        "setup_front_office_source_edit/<pk>",
        views.setup_front_office_source_edit,
        name="setup_front_office_source_edit",
    ),
    path(
        "setup_front_office_source_delete/<pk>",
        views.setup_front_office_source_delete,
        name="setup_front_office_source_delete",
    ),
    path(
        "setup_front_office_reference",
        views.setup_front_office_reference,
        name="setup_front_office_reference",
    ),
    path(
        "setup_front_office_reference_edit/<pk>",
        views.setup_front_office_reference_edit,
        name="setup_front_office_reference_edit",
    ),
    path(
        "setup_front_office_reference_delete/<pk>",
        views.setup_front_office_reference_delete,
        name="setup_front_office_reference_delete",
    ),
    path("student_details", views.student_details, name="student_details"),
    # student admission need to add rajji
    path("student_admission", views.student_admission, name="student_admission"),
    path("online_admission", views.online_admission, name="online_admission"),
    path("disabled_students", views.disabled_students, name="disabled_students"),
    path("multi_class_student", views.multi_class_student, name="multi_class_student"),
    path("bulk_delete", views.bulk_delete, name="bulk_delete"),
    # Till this send to raji
    path("student_category", views.student_category, name="student_category"),
    path(
        "student_category_edit/<pk>",
        views.student_category_edit,
        name="student_category_edit",
    ),
    path(
        "student_category_view/<pk>",
        views.student_category_view,
        name="student_category_view",
    ),
    path(
        "student_category_delete/<pk>",
        views.student_category_delete,
        name="student_category_delete",
    ),
    path("student_house", views.student_house, name="student_house"),
    path(
        "student_house_edit/<pk>", views.student_house_edit, name="student_house_edit"
    ),
    path(
        "student_house_view/<pk>", views.student_house_view, name="student_house_view"
    ),
    path(
        "student_house_delete/<pk>",
        views.student_house_delete,
        name="student_house_delete",
    ),
    path("disabled_reason", views.disabled_reason, name="disabled_reason"),
    path(
        "disabled_reason_edit/<pk>",
        views.disabled_reason_edit,
        name="disabled_reason_edit",
    ),
    path(
        "disabled_reason_view/<pk>",
        views.disabled_reason_view,
        name="disabled_reason_view",
    ),
    path(
        "disabled_reason_delete/<pk>",
        views.disabled_reason_delete,
        name="disabled_reason_delete",
    ),
    path("collect_fees", views.collect_fees, name="collect_fees"), 
    path("class_students", views.class_students, name="class_students"),
    # path('collect_fees_edit/<pk>', views.collect_fees_edit,name='collect_fees_edit'),
    # path('collect_fees_view/<pk>', views.collect_fees_view,name='collect_fees_view'),
    # path('collect_fees_delete/<pk>', views.collect_fees_delete,name='collect_fees_delete'),
    path(
        "collect_fees_detail/<pk>",
        views.collect_fees_detail,
        name="collect_fees_detail",
    ),
    path("search_fee_payment", views.search_fee_payment, name="search_fee_payment"),
    path("search_due_fee", views.search_due_fee, name="search_due_fee"),
    path("fees_master", views.fees_master, name="fees_master"),
    path("discount_js", views.discount_js, name="discount_js"),
    # path('get_total_fees/<int:fees_group_id>/', views.get_total_fees, name='get_total_fees'),
    # path('get_fee_options/<int:fees_group_id>/', views.get_fee_options, name='get_fee_options'),
    path(
        "fees_master_assign/<pk>", views.fees_master_assign, name="fees_master_assign"
    ),
    path(
        "fees_master_assign_js",
        views.fees_master_assign_js,
        name="fees_master_assign_js",
    ),
    path("fees_master_edit/<pk>", views.fees_master_edit_1, name="fees_master_edit"),
    path("fees_master_view/<pk>", views.fees_master_view, name="fees_master_view"),
    path(
        "fees_master_delete/<pk>", views.fees_master_delete, name="fees_master_delete"
    ),
    path("fees_master_edit", views.fees_master_edit, name="fees_master_edit"),
    path("fees_group", views.fees_group, name="fees_group"),
    path("fees_group_edit/<pk>", views.fees_group_edit, name="fees_group_edit"),
    path("fees_group_view/<pk>", views.fees_group_view, name="fees_group_view"),
    path("fees_group_delete/<pk>", views.fees_group_delete, name="fees_group_delete"),
    path("fees_type", views.fees_type, name="fees_type"),
    path("fees_type_edit/<pk>", views.fees_type_edit, name="fees_type_edit"),
    path("fees_type_view/<pk>", views.fees_type_view, name="fees_type_view"),
    path("fees_type_delete/<pk>", views.fees_type_delete, name="fees_type_delete"),
    path("fees_discount", views.fees_discount, name="fees_discount"),
    path(
        "fees_discount_edit/<pk>", views.fees_discount_edit, name="fees_discount_edit"
    ),
    path(
        "fees_discount_assign/<pk>",
        views.fees_discount_assign,
        name="fees_discount_assign",
    ),
    path(
        "fees_discount_delete/<pk>",
        views.fees_discount_delete,
        name="fees_discount_delete",
    ),
    path(
        "fees_discount_assign_js",
        views.fees_discount_assign_js,
        name="fees_discount_assign_js",
    ),
    path("fees_carry_forward", views.fees_carry_forward, name="fees_carry_forward"),
    path("fees_remainder", views.fees_remainder, name="fees_remainder"),
    path("add_income", views.add_income, name="add_income"),
    path("add_income_edit/<pk>", views.add_income_edit, name="add_income_edit"),
    path("add_income_view/<pk>", views.add_income_view, name="add_income_view"),
    path("add_income_delete/<pk>", views.add_income_delete, name="add_income_delete"),
    path("search_income", views.search_income, name="search_income"),
    path("income_head", views.income_head, name="income_head"),
    path("income_head_edit/<pk>", views.income_head_edit, name="income_head_edit"),
    path("income_head_view/<pk>", views.income_head_view, name="income_head_view"),
    path(
        "income_head_delete/<pk>", views.income_head_delete, name="income_head_delete"
    ),
    # expense
    path("add_expense", views.add_expense, name="add_expense"),
    path("add_expense_edit/<pk>", views.add_expense_edit, name="add_expense_edit"),
    path("add_expense_view/<pk>", views.add_expense_view, name="add_expense_view"),
    path(
        "add_expense_delete/<pk>", views.add_expense_delete, name="add_expense_delete"
    ),
    path("search_expense", views.search_expense, name="search_expense"),
    path("expense_head", views.expense_head, name="expense_head"),
    path("expense_head_edit/<pk>", views.expense_head_edit_1, name="expense_head_edit"),
    path("expense_head_view/<pk>", views.expense_head_view, name="expense_head_view"),
    path(
        "expense_head_delete/<pk>",
        views.expense_head_delete,
        name="expense_head_delete",
    ),
    # Accounts
    # Asset Type
    path("add_asset_type/", views.add_asset_type, name="add_asset_type"),
    path("view_asset_type/", views.view_asset_type, name="view_asset_type"),
    path("all_asset_type/", views.all_asset_type, name="all_asset_type"),
    # GlLine
    path("add_gline/", views.add_gline, name="add_gline"),
    path("view_gline/", views.view_gline, name="view_gline"),
    path("all_gline/", views.all_gline, name="all_gline"),
    path("add_gline_view/<pk>", views.add_gline_view, name="add_gline_view"),
    path("add_gline_edit/<pk>", views.add_gline_edit, name="add_gline_edit"),
    path(
        "add_gline_delete/<pk>", views.add_gline_delete, name="add_gline_delete"
    ),
    # Account Type
    path("add_account_type/", views.add_account_type, name="add_account_type"),
    path("view_account_type/", views.view_account_type, name="view_account_type"),
    path("all_account_type/", views.all_account_type, name="all_account_type"),
    path("account_type/", views.account_type, name="account_type"),
    path("account_type_edit/<pk>", views.account_type_edit, name="account_type_edit"),
    path("account_type_view/<pk>", views.account_type_view, name="account_type_view"),
    path("account_type_delete/<pk>", views.account_type_delete, name="account_type_delete"),
    # Account
    # path("add_account/", views.add_account, name="add_account"),
    # path("view_account/", views.view_account, name="view_account"),
    # path("all_account/", views.all_account, name="all_account"),
    path("add_account/", views.add_account, name="add_account"),
    path("view_account_edit/<pk>", views.view_account_edit, name="view_account_edit"),
    path("view_account_view/<pk>", views.view_account_view, name="view_account_view"),
    path("view_account_delete/<pk>", views.view_account_delete, name="view_account_delete"),
    # Transaction Screen
    path("add_transaction/", views.add_transaction, name="add_transaction"),
    path("view_transaction/", views.view_transaction, name="view_transaction"),
    path("all_transaction/", views.all_transaction, name="all_transaction"),
    # Transaction Code
    path(
        "add_transaction_code/", views.add_transaction_code, name="add_transaction_code"
    ),
    path(
        "view_transaction_code/",
        views.view_transaction_code,
        name="view_transaction_code",
    ),
    # Charge Type
    path("add_charge_type/", views.add_charge_type, name="add_charge_type"),
    path("view_charge_type/", views.view_charge_type, name="view_charge_type"),
    path("charge_type/", views.charge_type, name="charge_type"),
    path("charge_type_edit/<pk>", views.charge_type_edit, name="charge_type_edit"),
    path("charge_type_view/<pk>", views.charge_type_view, name="charge_type_view"),
    path("charge_type_delete/<pk>", views.charge_type_delete, name="charge_type_delete"),
    # Transaction Type
    path(
        "add_transaction_type/", views.add_transaction_type, name="add_transaction_type"
    ),
    path(
        "view_transaction_type/",
        views.view_transaction_type,
        name="view_transaction_type",
    ),
    # Account Entry
    # path("account_entry/", views.account_entry_view, name="account_entry"),
    # path('account_entry/', views.account_entry_view, name='account_entry'),
    # path("add_account_entry/", views.add_account_entry, name="add_account_entry"),
    # path("view_account_entry/", views.view_account_entry, name="view_account_entry"),
    # path("all_account_entry/", views.all_account_entry, name="all_account_entry"),
    
    path("account_entry/", views.account_entry, name="account_entry"),
    path("account_entry_edit/<pk>", views.account_entry_edit, name="account_entry_edit"),
    path("account_entry_view/<pk>", views.account_entry_view, name="account_entry_view"),
    path("account_entry_delete/<pk>", views.account_entry_delete, name="account_entry_delete"),
    # Attendance
    path("student_attendance", views.student_attendance, name="student_attendance"),
    path("approve_leave", views.approve_leave, name="approve_leave"),
    path(
        "approve_leave_edit/<pk>", views.approve_leave_edit, name="approve_leave_edit"
    ),
    path(
        "approve_leave_view/<pk>", views.approve_leave_view, name="approve_leave_view"
    ),
    path(
        "approve_leave_delete/<pk>",
        views.approve_leave_delete,
        name="approve_leave_delete",
    ),
    path("attendance_by_date", views.attendance_by_date, name="attendance_by_date"),
    # Examinations
    path("exam_group", views.exam_group, name="exam_group"),
    path("exam_group_edit/<pk>", views.exam_group_edit, name="exam_group_edit"),
    path("exam_group_view/<pk>", views.exam_group_view, name="exam_group_view"),
    path("exam_group_delete/<pk>", views.exam_group_delete, name="exam_group_delete"),
    path("exam_schedule", views.exam_schedule, name="exam_schedule"),
    path("exam_result", views.exam_result, name="exam_result"),
    path("design_admit_card", views.design_admit_card, name="design_admit_card"),
    path(
        "design_admit_card_edit/<pk>",
        views.design_admit_card_edit,
        name="design_admit_card_edit",
    ),
    path(
        "design_admit_card_view/<pk>",
        views.design_admit_card_view,
        name="design_admit_card_view",
    ),
    path(
        "design_admit_card_delete/<pk>",
        views.design_admit_card_delete,
        name="design_admit_card_delete",
    ),
    path("print_admit_card", views.print_admit_card, name="print_admit_card"),
    path("design_marksheet", views.design_marksheet, name="design_marksheet"),
    path(
        "design_marksheet_edit/<pk>",
        views.design_marksheet_edit,
        name="design_marksheet_edit",
    ),
    path(
        "design_marksheet_view/<pk>",
        views.design_marksheet_view,
        name="design_marksheet_view",
    ),
    path(
        "design_marksheet_delete/<pk>",
        views.design_marksheet_delete,
        name="design_marksheet_delete",
    ),
    path("print_marksheet", views.print_marksheet, name="print_marksheet"),
    path("marks_grade", views.marks_grade, name="marks_grade"),
    path("marks_grade_edit/<pk>", views.marks_grade_edit, name="marks_grade_edit"),
    path("marks_grade_view/<pk>", views.marks_grade_view, name="marks_grade_view"),
    path(
        "marks_grade_delete/<pk>", views.marks_grade_delete, name="marks_grade_delete"
    ),
    #
    path("assign_subject", views.assign_subject, name="assign_subject"),
    path(
        "assign_subject_edit/<pk>",
        views.assign_subject_edit,
        name="assign_subject_edit",
    ),
    path(
        "assign_subject_view/<pk>",
        views.assign_subject_view,
        name="assign_subject_view",
    ),
    path(
        "assign_subject_delete/<pk>",
        views.assign_subject_delete,
        name="assign_subject_delete",
    ),
    # 68
    # Online Exam
    path("online_exam", views.online_exam, name="online_exam"),
    path("online_exam_edit/<pk>", views.online_exam_edit, name="online_exam_edit"),
    path("online_exam_view/<pk>", views.online_exam_view, name="online_exam_view"),
    path(
        "online_exam_delete/<pk>", views.online_exam_delete, name="online_exam_delete"
    ),
    path("question_bank", views.question_bank, name="question_bank"),
    path(
        "question_bank_edit/<pk>", views.question_bank_edit, name="question_bank_edit"
    ),
    path(
        "question_bank_view/<pk>", views.question_bank_view, name="question_bank_view"
    ),
    path(
        "question_bank_delete/<pk>",
        views.question_bank_delete,
        name="question_bank_delete",
    ),
    # Lesson PLAN
    path("manage_lesson_plan", views.manage_lesson_plan, name="manage_lesson_plan"),
    path("lesson", views.lesson, name="lesson"),
    path("lesson_edit/<sub>", views.lesson_edit, name="lesson_edit"),
    path("lesson_view/<sub>", views.lesson_view, name="lesson_view"),
    path("lesson_delete/<pk>", views.lesson_delete, name="lesson_delete"),
    path(
        "lesson_bulk_delete/<sub>", views.lesson_bulk_delete, name="lesson_bulk_delete"
    ),
    path("topicc", views.topicc, name="topicc"),
    path("topicc_edit/<pk>", views.topicc_edit, name="topicc_edit"),
    path("topicc_view/<pk>", views.topicc_view, name="topicc_view"),
    path("topicc_delete/<pk>", views.topicc_delete, name="topicc_delete"),
    path("topic_bulk_delete/<pk>", views.topic_bulk_delete, name="topic_bulk_delete"),
    # Academics
    path(
        "assign_class_teacher", views.assign_class_teacher, name="assign_class_teacher"
    ),
    path(
        "assign_class_teacher_edit/<pk>",
        views.assign_class_teacher_edit,
        name="assign_class_teacher_edit",
    ),
    path(
        "assign_class_teacher_view/<pk>",
        views.assign_class_teacher_view,
        name="assign_class_teacher_view",
    ),
    path(
        "assign_class_teacher_delete/<pk>",
        views.assign_class_teacher_delete,
        name="assign_class_teacher_delete",
    ),
    #assign subject teacher
       path(
        "assign_subject_teacher", views.assign_subject_teacher, name="assign_subject_teacher"
    ),
    path(
        "assign_subject_teacher_edit/<pk>",
        views.assign_subject_teacher_edit,
        name="assign_subject_teacher_edit",
    ),
    path(
        "assign_subject_teacher_view/<pk>",
        views.assign_subject_teacher_view,
        name="assign_subject_teacher_view",
    ),
    path(
        "assign_subject_teacher_delete/<pk>",
        views.assign_subject_teacher_delete,
        name="assign_subject_teacher_delete",
    ),
    path("promote_students", views.promote_students, name="promote_students"),
    path("class_timetable", views.class_timetable, name="class_timetable"),
    path("timetable_save_js", views.timetable_save_js, name="timetable_save_js"),
    path(
        "class_timetable_view", views.class_timetable_view, name="class_timetable_view"
    ),
    path("timetable_delete", views.timetable_delete, name="timetable_delete"),
    path("teacher_timetable", views.teacher_timetable, name="teacher_timetable"),
    path("section_js", views.section_js, name="section_js"),
    path("subject_group", views.subject_group, name="subject_group"),
    path(
        "subject_group_edit/<pk>", views.subject_group_edit, name="subject_group_edit"
    ),
    path(
        "subject_group_view/<pk>", views.subject_group_view, name="subject_group_view"
    ),
    path(
        "subject_group_delete/<pk>",
        views.subject_group_delete,
        name="subject_group_delete",
    ),
    path("subjects", views.subjects, name="subjects"),
    path("subjects_edit/<pk>", views.subjects_edit, name="subjects_edit"),
    path("subjects_view/<pk>", views.subjects_view, name="subjects_view"),
    path("subjects_delete/<pk>", views.subjects_delete, name="subjects_delete"),
    path("Classes", views.Classes, name="Classes"),
    path("Classes_edit/<pk>", views.Classes_edit, name="Classes_edit"),
    path("Classes_view/<pk>", views.Classes_view, name="Classes_view"),
    path("Classes_delete/<pk>", views.Classes_delete, name="Classes_delete"),
    path("sections", views.sections, name="sections"),
    path("sections_edit/<pk>", views.sections_edit, name="sections_edit"),
    path("sections_view/<pk>", views.sections_view, name="sections_view"),
    path("sections_delete/<pk>", views.sections_delete, name="sections_delete"),
    # class register
    path("class_register", views.class_register, name="class_register"),
    path(
        "class_register_edit/<pk>",
        views.class_register_edit,
        name="class_register_edit",
    ),
    path(
        "class_register_view/<pk>",
        views.class_register_view,
        name="class_register_view",
    ),
    path(
        "class_register_delete/<pk>",
        views.class_register_delete,
        name="class_register_delete",
    ),
    # educationlevel
    # school composition
    path("school_composition1", views.school_composition1, name="school_compositions"),
    path("school_compositions", views.school_compositions, name="school_compositions"),
    path(
        "school_composition_edit/<pk>",
        views.school_composition_edit,
        name="school_composition_edit",
    ),
    path(
        "school_composition_view/<pk>",
        views.school_composition_view,
        name="school_composition_view",
    ),
    path(
        "school_composition_delete/<pk>",
        views.school_composition_delete,
        name="school_composition_delete",
    ),
    # education level
    path("education_level1", views.education_level1, name="education_levels"),
    path("education_levels", views.education_levels, name="education_levels"),
    path(
        "education_level_edit/<pk>",
        views.education_level_edit,
        name="education_level_edit",
    ),
    path(
        "education_level_view/<pk>",
        views.education_level_view,
        name="education_level_view",
    ),
    path(
        "education_level_delete/<pk>",
        views.education_level_delete,
        name="education_level_delete",
    ),
    # Structure
    # curriculum
    path("curriculums", views.curriculums, name="curriculums"),
    path("curriculum_edit/<pk>", views.curriculum_edit, name="curriculum_edit"),
    path("curriculum_delete/<pk>", views.curriculum_delete, name="curriculum_delete"),
    # branch
    path("branch1", views.branch1, name="branch1"),
    path("branch", views.branch, name="branch"),
    path("branch_edit/<pk>", views.branch_edit, name="branch_edit"),
    path("branch_view/<pk>", views.branch_view, name="branch_view"),
    path("branch_delete/<pk>", views.branch_delete, name="branch_delete"),
    # company
    path("company", views.company, name="company"),
    path("company_edit/<pk>", views.company_edit, name="company_edit"),
    # path("company_view/<pk>", views.company_view, name="company_view"),
    path("company_delete/<pk>", views.company_delete, name="company_delete"),
    # school
    path("school1", views.school1, name="schools"),
    path("schools", views.schools, name="schools"),
    path("school_edit/<pk>", views.school_edit, name="school_edit"),
    path("school_view/<pk>", views.school_view, name="school_view"),
    path("school_delete/<pk>", views.school_delete, name="school_delete"),
    # shool year eg 2024
    path("school_year1", views.school_year1, name="school_year1"),
    path("school_years", views.school_years, name="school_years"),
    path("school_year_edit/<pk>", views.school_year_edit, name="school_year_edit"),
    path("school_year_view/<pk>", views.school_year_view, name="school_year_view"),
    path(
        "school_year_delete/<pk>", views.school_year_delete, name="school_year_delete"
    ),
    # shool term eg first term
    path("school_term1", views.school_term1, name="school_terms"),
    path("school_terms", views.school_terms, name="school_terms"),
    path("school_term_edit/<pk>", views.school_term_edit, name="school_term_edit"),
    path("school_term_view/<pk>", views.school_term_view, name="school_term_view"),
    path(
        "school_term_delete/<pk>", views.school_term_delete, name="school_term_delete"
    ),
    # grading system
    path("grading_system1", views.grading_system1, name="grading_systems"),
    path("grading_systems", views.grading_systems, name="grading_systems"),
    path(
        "grading_system_edit/<pk>",
        views.grading_system_edit,
        name="grading_system_edit",
    ),
    path(
        "grading_system_view/<pk>",
        views.grading_system_view,
        name="grading_system_view",
    ),
    path(
        "grading_system_delete/<pk>",
        views.grading_system_delete,
        name="grading_system_delete",
    ),
    # Human Resource
    path("add_staff", views.add_staff, name="add_staff"),
    path(
        "approve_leave_request",
        views.approve_leave_request,
        name="approve_leave_request",
    ),
    path(
        "approve_leave_request_edit/<pk>",
        views.approve_leave_request_edit,
        name="approve_leave_request_edit",
    ),
    path(
        "approve_leave_request_delete/<pk>",
        views.approve_leave_request_delete,
        name="approve_leave_request_delete",
    ),
    path("apply_leave", views.apply_leave, name="apply_leave"),
    path("apply_leave_edit/<pk>", views.apply_leave_edit, name="apply_leave_edit"),
    path(
        "apply_leave_delete/<pk>", views.apply_leave_delete, name="apply_leave_delete"
    ),
    path("add_leave_type", views.add_leave_type, name="add_leave_type"),
    path(
        "add_leave_type_delete/<pk>",
        views.add_leave_type_delete,
        name="add_leave_type_delete",
    ),
    path(
        "add_leave_type_edit/<pk>",
        views.add_leave_type_edit,
        name="add_leave_type_edit",
    ),
    path(
        "teachers_rating_list", views.teachers_rating_list, name="teachers_rating_list"
    ),
    path(
        "teachers_rating_list", views.teachers_rating_list, name="teachers_rating_list"
    ),
    path("department", views.department, name="department"),
    path("department_edit/<pk>", views.department_edit, name="department_edit"),
    path(
        "department_delete<int:pk>", views.department_delete, name="department_delete"
    ),
    path("designation", views.designation, name="designation"),
    path("designation_edit/<pk>", views.designation_edit, name="designation_edit"),
    path(
        "designation_delete/<pk>", views.designation_delete, name="designation_delete"
    ),
    # Communicate
    path("notice_board", views.notice_board, name="notice_board"),
    path("notice_board_edit<pk>", views.notice_board_edit, name="notice_board_edit"),
    path(
        "notice_board_delete<pk>", views.notice_board_delete, name="notice_board_delete"
    ),
    path("email_sms_log", views.email_sms_log, name="email_sms_log"),
    # Download Center
    path("upload_content", views.upload_content, name="upload_content"),
    path(
        "upload_content_edit<pk>", views.upload_content_edit, name="upload_content_edit"
    ),
    path(
        "upload_content_delete<pk>",
        views.upload_content_delete,
        name="upload_content_delete",
    ),
    path("assignment_list", views.assignment_list, name="assignment_list"),
    path(
        "assignment_list_delete<pk>",
        views.assignment_list_delete,
        name="assignment_list_delete",
    ),
    path("study_material", views.study_material, name="study_material"),
    path(
        "study_material_delete<pk>",
        views.study_material_delete,
        name="study_material_delete",
    ),
    path("syllabus", views.syllabus, name="syllabus"),
    path("syllabus_delete<pk>", views.syllabus_delete, name="syllabus_delete"),
    path("other_download_list", views.other_download_list, name="other_download_list"),
    path(
        "other_download_list_delete<pk>",
        views.other_download_list_delete,
        name="other_download_list_delete",
    ),
    path("add_homework", views.add_homework, name="add_homework"),
    path("book_list", views.book_list, name="book_list"),
    path("book_list_edit/<pk>", views.book_list_edit, name="book_list_edit"),
    path("book_list_delete/<pk>", views.book_list_delete, name="book_list_delete"),
    path("member_book_issue/<pk>", views.member_book_issued, name="member_book_issued"),
    path("add_staff_member", views.add_staff_member, name="add_staff_member"),
    path("add_student_member", views.add_student_member, name="add_student_member"),
    path("book_issuse_return", views.book_issuse_return, name="book_issuse_return"),
    path("book_qty_js", views.book_qty_js, name="book_qty_js"),
    path("book_return/<pk>", views.book_return, name="book_return"),
    path(
        "libary_surrender_card/<pk>",
        views.libary_surrender_card,
        name="libary_surrender_card",
    ),
    # Inventory
    path("issue_item", views.issue_item, name="issue_item"),
    path("issue_item_delete/<pk>", views.issue_item_delete, name="issue_item_delete"),
    path("add_item_stock", views.add_item_stock, name="add_item_stock"),
    path(
        "add_item_stock_delete/<pk>",
        views.add_item_stock_delete,
        name="add_item_stock_delete",
    ),
    path(
        "add_item_stock_edit/<pk>",
        views.add_item_stock_edit,
        name="add_item_stock_edit",
    ),
    # Assign To Raji
    path("add_item", views.add_item, name="add_item"),
    path("add_item_view/<pk>", views.add_item_view, name="add_item_view"),
    path("add_item_delete/<pk>", views.add_item_delete, name="add_item_delete"),
    path("add_item_edit/<pk>", views.add_item_edit, name="add_item_edit"),
    path("add_item_category", views.add_item_category, name="add_item_category"),
    path(
        "add_item_category_view/<pk>",
        views.add_item_category_view,
        name="add_item_category_view",
    ),
    path(
        "add_item_category_delete/<pk>",
        views.add_item_category_delete,
        name="add_item_category_delete",
    ),
    path(
        "add_item_category_edit/<pk>",
        views.add_item_category_edit,
        name="add_item_category_edit",
    ),
    path("item_store", views.item_store, name="item_store"),
    path("item_store_view/<pk>", views.item_store_view, name="item_store_view"),
    path("item_store_delete/<pk>", views.item_store_delete, name="item_store_delete"),
    path("item_store_edit/<pk>", views.item_store_edit, name="item_store_edit"),
    path("item_supplier", views.item_supplier, name="item_supplier"),
    path(
        "item_supplier_view/<pk>", views.item_supplier_view, name="item_supplier_view"
    ),
    path(
        "item_supplier_delete/<pk>",
        views.item_supplier_delete,
        name="item_supplier_delete",
    ),
    path(
        "item_supplier_edit/<pk>", views.item_supplier_edit, name="item_supplier_edit"
    ),
    path("routes", views.routes, name="routes"),
    path("routes_view/<pk>", views.routes_view, name="routes_view"),
    path("routes_delete/<pk>", views.routes_delete, name="routes_delete"),
    path("routes_edit/<pk>", views.routes_edit, name="routes_edit"),
    path("vehicle", views.vehicle, name="vehicle"),
    path("vehicle_view/<pk>", views.vehicle_view, name="vehicle_view"),
    path("vehicle_delete/<pk>", views.vehicle_delete, name="vehicle_delete"),
    path("vehicle_edit/<pk>", views.vehicle_edit, name="vehicle_edit"),
    path("assign_vehicle", views.assign_vehicle, name="assign_vehicle"),
    path(
        "assign_vehicle_view/<pk>",
        views.assign_vehicle_view,
        name="assign_vehicle_view",
    ),
    path(
        "assign_vehicle_delete/<pk>",
        views.assign_vehicle_delete,
        name="assign_vehicle_delete",
    ),
    path(
        "assign_vehicle_edit/<pk>",
        views.assign_vehicle_edit,
        name="assign_vehicle_edit",
    ),
    path("hostel_room", views.hostel_room, name="hostel_room"),
    path("hostel_room_view/<pk>", views.hostel_room_view, name="hostel_room_view"),
    path(
        "hostel_room_delete/<pk>", views.hostel_room_delete, name="hostel_room_delete"
    ),
    path("hostel_room_edit/<pk>", views.hostel_room_edit, name="hostel_room_edit"),
    path("room_type", views.room_type, name="room_type"),
    path("room_type_view/<pk>", views.room_type_view, name="room_type_view"),
    path("room_type_delete/<pk>", views.room_type_delete, name="room_type_delete"),
    path("room_type_edit/<pk>", views.room_type_edit, name="room_type_edit"),
    path("hostel", views.hostel, name="hostel"),
    path("hostel_view/<pk>", views.hostel_view, name="hostel_view"),
    path("hostel_delete/<pk>", views.hostel_delete, name="hostel_delete"),
    path("hostel_edit/<pk>", views.hostel_edit, name="hostel_edit"),
    # TODAY
    path("student_certificate", views.student_certificate, name="student_certificate"),
    path(
        "student_certificate_view/<pk>",
        views.student_certificate_view,
        name="student_certificate_view",
    ),
    path(
        "student_certificate_delete/<pk>",
        views.student_certificate_delete,
        name="student_certificate_delete",
    ),
    path(
        "student_certificate_edit/<pk>",
        views.student_certificate_edit,
        name="student_certificate_edit",
    ),
    path("student_id_card", views.student_id_card, name="student_id_card"),
    path(
        "student_id_card_view/<pk>",
        views.student_id_card_view,
        name="student_id_card_view",
    ),
    path(
        "student_id_card_delete/<pk>",
        views.student_id_card_delete,
        name="student_id_card_delete",
    ),
    path(
        "student_id_card_edit/<pk>",
        views.student_id_card_edit,
        name="student_id_card_edit",
    ),
    path("add_event", views.add_event, name="add_event"),
    path("media_manager", views.media_manager, name="media_manager"),
    path(
        "media_manager_view/<pk>", views.media_manager_view, name="media_manager_view"
    ),
    path(
        "media_manager_delete/<pk>",
        views.media_manager_delete,
        name="media_manager_delete",
    ),
    path(
        "media_manager_edit/<pk>", views.media_manager_edit, name="media_manager_edit"
    ),
    path("menus", views.menus, name="menus"),
    path("menus_view/<pk>", views.menus_view, name="menus_view"),
    path("menus_delete/<pk>", views.menus_delete, name="menus_delete"),
    path("menus_edit/<pk>", views.menus_edit, name="menus_edit"),
    path("alumni_events", views.alumni_events, name="alumni_events"),
    path(
        "alumni_events_view/<pk>", views.alumni_events_view, name="alumni_events_view"
    ),
    path(
        "alumni_events_delete/<pk>",
        views.alumni_events_delete,
        name="alumni_events_delete",
    ),
    path(
        "alumni_events_edit/<pk>", views.alumni_events_edit, name="alumni_events_edit"
    ),
    path("alumni_events_add", views.alumni_events_add, name="alumni_events_add"),
    path("session", views.session, name="session"),
    path("session_view/<pk>", views.session_view, name="session_view"),
    path("session_delete/<pk>", views.session_delete, name="session_delete"),
    path("session_edit/<pk>", views.session_edit, name="session_edit"),
    path("role", views.role, name="role"),
    path("role_view/<pk>", views.role_view, name="role_view"),
    path("role_delete/<pk>", views.role_delete, name="role_delete"),
    path("role_edit/<pk>", views.role_edit, name="role_edit"),
    path("student_list_view/<pk>", views.student_list_view, name="student_list_view"),
    path(
        "student_list_delete/<pk>",
        views.student_list_delete,
        name="student_list_delete",
    ),
    path(
        "student_information_report",
        views.student_information_report,
        name="student_information_report",
    ),
    path("guardian_report", views.guardian_report, name="guardian_report"),
    path(
        "student_history_report",
        views.student_history_report,
        name="student_history_report",
    ),
    path("disable_enable", views.disable_enable, name="disable_enable"),
    path("add_issue_item", views.add_issue_item, name="add_issue_item"),
    #
    path(
        "non_returnable_items/",
        views.non_returnable_items_view,
        name="non_returnable_items_view",
    ),
    path("item_js", views.item_js, name="item_js"),
    path("item_available_js", views.item_available_js, name="item_available_js"),
    path(
        "leave_approve_disappove/<pk>",
        views.leave_approve_disappove,
        name="leave_approve_disappove",
    ),
    path("addexamlist/<pk>", views.addexamlist, name="addexamlist"),
    path("addexamlist_edit/<pk>", views.addexamlist_edit, name="addexamlist_edit"),
    path(
        "addexamlist_delete/<pk>", views.addexamlist_delete, name="addexamlist_delete"
    ),
    path(
        "assign_view_student/<pk>",
        views.assign_view_student,
        name="assign_view_student",
    ),
    path("addexamsubject/<pk>", views.addexamsubject, name="addexamsubject"),
    path(
        "delete_exam_subjects/<pk>",
        views.delete_exam_subjects,
        name="delete_exam_subjects",
    ),
    path("addexammark/<pk>", views.addexammark, name="addexammark"),
    path("enter_mark/<pk>", views.enter_mark, name="enter_mark"),
    path("staff_directory", views.staff_directory, name="staff_directory"),
    path(
        "Staff_details_show/<pk>", views.Staff_details_show, name="Staff_details_show"
    ),
    path(
        "staff_disable_enable", views.staff_disable_enable, name="staff_disable_enable"
    ),
    path("add_staffs_edit/<pk>", views.add_staffs_edit, name="add_staffs_edit"),
    path(
        "staff_attendance_view",
        views.staff_attendance_view,
        name="staff_attendance_view",
    ),
    path("payroll", views.payroll, name="payroll"),
    path("payroll_view/<pk>", views.payroll_view, name="payroll_view"),
    path("payroll_piad/<pk>", views.payroll_piad, name="payroll_piad"),
    path("Payroll_payslip/<pk>", views.Payroll_payslip, name="Payroll_payslip"),
    path("Human_Resource", views.Human_Resource, name="Human_Resource"),
    path("payroll_report", views.payroll_report, name="payroll_report"),
    path("search_due_fee", views.search_due_fee, name="search_due_fee"),
    path("mange_alumini", views.mange_alumini, name="mange_alumini"),
    path("Mange_alumini_add/<pk>", views.Mange_alumini_add, name="Mange_alumini_add"),
    path(
        "Mange_alumini_edit/<pk>", views.Mange_alumini_edit, name="Mange_alumini_edit"
    ),
    path(
        "Mange_alumini_delete/<pk>",
        views.Mange_alumini_delete,
        name="Mange_alumini_delete",
    ),
    path(
        "mange_alumini_report", views.mange_alumini_report, name="mange_alumini_report"
    ),
    path("hostel_repoert", views.hostel_repoert, name="hostel_repoert"),
    path("transport_report", views.transport_report, name="transport_report"),
    path("book_isseu_report", views.book_isseu_report, name="book_isseu_report"),
    path(
        "book_inventory_report",
        views.book_inventory_report,
        name="book_inventory_report",
    ),
    path("book_due_report", views.book_due_report, name="book_due_report"),
    path(
        "book_issue_return_report",
        views.book_issue_return_report,
        name="book_issue_return_report",
    ),
    path("library", views.library, name="library"),
    path("Inventory", views.Inventory, name="Inventory"),
    path("issue_item_report", views.issue_item_report, name="issue_item_report"),
    path("stock_report", views.stock_report, name="stock_report"),
    path("Add_item_report", views.Add_item_report, name="Add_item_report"),
    path("attendence", views.attendence, name="attendence"),
    path("attendence_report", views.attendence_report, name="attendence_report"),
    path(
        "staff_attendance_report",
        views.staff_attendance_report,
        name="staff_attendance_report",
    ),
    path(
        "daily_attendance_report",
        views.daily_attendance_report,
        name="daily_attendance_report",
    ),
    path(
        "student_attendance_type_report",
        views.student_attendance_type_report,
        name="student_attendance_type_report",
    ),
    path("demo_js", views.demo_js, name="demo_js"),
    path("leave_type_js", views.leave_type_js, name="leave_type_js"),
    path("mark_save/<pk>", views.mark_save, name="mark_save"),
    path("exam_js", views.exam_js, name="exam_js"),
    path("general_setting", views.general_setting, name="general_setting"),
    path("student_js", views.student_js, name="student_js"),
    path("subject_grp_js", views.subject_grp_js, name="subject_grp_js"),
    path("subject_js", views.subject_js, name="subject_js"),
    path("topic_js", views.topic_js, name="topic_js"),
    path(
        "manage_syllabus_status",
        views.manage_syllabus_status,
        name="manage_syllabus_status",
    ),
    path("add_homework_edit/<pk>", views.add_homework_edit, name="add_homework_edit"),
    path("add_homework_view/<pk>", views.add_homework_view, name="add_homework_view"),
    path(
        "add_homework_delete/<pk>",
        views.add_homework_delete,
        name="add_homework_delete",
    ),
    # website part
    path("web_index", views.web_index, name="web_index"),
    path("basic_detail", views.basic_detail, name="basic_detail"),
    path("carousel", views.carousel, name="carousel"),
    path("carousel_edit/<pk>", views.carousel_edit, name="carousel_edit"),
    path("carousel_delete/<pk>", views.carousel_delete, name="carousel_delete"),
    path("infrastructure", views.infrastructure, name="infrastructure"),
    path(
        "infrastructure_edit<pk>", views.infrastructure_edit, name="infrastructure_edit"
    ),
    path(
        "infrastructure_delete<pk>",
        views.infrastructure_delete,
        name="infrastructure_delete",
    ),
    path("school_staff", views.school_staff, name="school_staff"),
    path("school_staff_edit<pk>", views.school_staff_edit, name="school_staff_edit"),
    path(
        "school_staff_delete<pk>", views.school_staff_delete, name="school_staff_delete"
    ),
    path("school_head", views.school_head, name="school_head"),
    path("school_head_edit<pk>", views.school_head_edit, name="school_head_edit"),
    path("school_head_delete<pk>", views.school_head_delete, name="school_head_delete"),
    path("news", views.news, name="news"),
    path("news_edit/<pk>", views.news_edit, name="news_edit"),
    path("news_delete/<pk>", views.news_delete, name="news_delete"),
    path("offers", views.offers, name="offers"),
    path("offers_edit/<pk>", views.offers_edit, name="offers_edit/<pk>"),
    path("offers_delete<pk>", views.offers_delete, name="offers_delete<pk>"),
    path("event", views.event, name="event"),
    path("event_view/<pk>", views.event_view, name="event_view"),
    path("event_delete/<pk>", views.event_delete, name="event_delete"),
    path("event_edit/<pk>", views.event_edit, name="event_edit"),
    path("assign_permission/<pk>", views.assign_permission, name="assign_permission"),
    path("disabled_staff", views.disabled_staff, name="disabled_staff"),
    path("student_report_js", views.student_report_js, name="student_report_js"),
    path("printing_admit_card", views.printing_admit_card, name="printing_admit_card"),
    path("printing_marksheet", views.printing_marksheet, name="printing_marksheet"),
    path("generate_ID_card", views.generate_ID_card, name="generate_ID_card"),
    path("print_ID_card", views.print_ID_card, name="print_ID_card"),
    path(
        "teacher_rating_approval/<pk>",
        views.teacher_rating_approval,
        name="teacher_rating_approval",
    ),
    path(
        "teacher_rating_delete/<pk>",
        views.teacher_rating_delete,
        name="teacher_rating_delete",
    ),
    path("admission_report", views.admission_report, name="admission_report"),
    path(
        "balances_fees_report", views.balances_fees_report, name="balances_fees_report"
    ),
    path(
        "class_subject_report", views.class_subject_report, name="class_subject_report"
    ),
    path("examinations_report", views.examinations_report, name="examinations_report"),
    path(
        "expense_group_report", views.expense_group_report, name="expense_group_report"
    ),
    path("expense_report", views.expense_report, name="expense_report"),
    path(
        "fees_collection_report",
        views.fees_collection_report,
        name="fees_collection_report",
    ),
    path("Finances_report", views.Finances_report, name="Finances_report"),
    path(
        "homework_evaluation_report",
        views.homework_evaluation_report,
        name="homework_evaluation_report",
    ),
    path("income_group_report", views.income_group_report, name="income_group_report"), 
    path("income_report", views.income_report, name="income_report"),
    path("net_profit_loss_report", views.net_profit_loss_report, name="net_profit_loss_report"),
    path(
        "Report_payroll_report",
        views.Report_payroll_report,
        name="Report_payroll_report",
    ),
    path("sibling_report", views.sibling_report, name="sibling_report"),
    path(
        "student_gender_ratio_report",
        views.student_gender_ratio_report,
        name="student_gender_ratio_report",
    ),
    path(
        "student_teacher_ratio_report",
        views.student_teacher_ratio_report,
        name="student_teacher_ratio_report",
    ),
    path(
        "student_profile_report",
        views.student_profile_report,
        name="student_profile_report",
    ),
    path("send_email", views.send_email, name="send_email"),
    path("get_sections/", views.get_sections, name="get_sections"),
    path(
        "manage_lesson_topic_js",
        views.manage_lesson_topic_js,
        name="manage_lesson_topic_js",
    ),
    path("manage_lesson_save", views.manage_lesson_save, name="manage_lesson_save"),
    path(
        "edit_manage_lesson_js",
        views.edit_manage_lesson_js,
        name="edit_manage_lesson_js",
    ),
    path(
        "manage_lesson_delete/<pk>",
        views.manage_lesson_delete,
        name="manage_lesson_delete",
    ),
    path(
        "syllabus_status_report",
        views.syllabus_status_report,
        name="syllabus_status_report",
    ),
    path(
        "student_report_finances_js",
        views.student_report_finances_js,
        name="student_report_finances_js",
    ),
    path("import_student", views.import_student, name="import_student"),
    path("import_staff", views.import_staff, name="import_staff"),
    path(
        "student_login_credentials",
        views.student_login_credentials,
        name="student_login_credentials",
    ),
    path(
        "subject_lesson_paln_report",
        views.subject_lesson_paln_report,
        name="subject_lesson_paln_report",
    ),
    path(
        "generate_student_certificate",
        views.generate_student_certificate,
        name="generate_student_certificate",
    ),
    path(
        "printing_student_certificate",
        views.printing_student_certificate,
        name="printing_student_certificate",
    ),
    path("profile", views.profile, name="profile"),
    path("indvidula_send_mail", views.indvidula_send_mail, name="indvidula_send_mail"),
    path("send_mail_search_js", views.send_mail_search_js, name="send_mail_search_js"),
    path("mail_search_save_js", views.mail_search_save_js, name="mail_search_save_js"),
    path(
        "mail_search_delete_js",
        views.mail_search_delete_js,
        name="mail_search_delete_js",
    ),
    path("online_class", views.online_class, name="online_class"),
    path("online_class_edit/<pk>", views.online_class_edit, name="online_class_edit"),
    path(
        "online_class_delete/<pk>",
        views.online_class_delete,
        name="online_class_delete",
    ),
    path("staff_meeting", views.staff_meeting, name="staff_meeting"),
    path(
        "staff_meeting_edit/<pk>", views.staff_meeting_edit, name="staff_meeting_edit"
    ),
    path(
        "staff_meeting_delete/<pk>",
        views.staff_meeting_delete,
        name="staff_meeting_delete",
    ),
    path("parent_meeting", views.parent_meeting, name="parent_meeting"),
    path(
        "parent_meeting_edit/<pk>",
        views.parent_meeting_edit,
        name="parent_meeting_edit",
    ),
    path(
        "parent_meeting_delete/<pk>",
        views.parent_meeting_delete,
        name="parent_meeting_delete",
    ),
    path(
        "staff_meetimg_backup/<pk>",
        views.staff_meetimg_backup,
        name="staff_meetimg_backup",
    ),
    path(
        "staff_meeting_view/<pk>", views.staff_meeting_view, name="staff_meeting_view"
    ),
    path(
        "student_details_edit/<pk>",
        views.student_details_edit,
        name="student_details_edit",
    ),
    path(
        "student_details_delete/<pk>",
        views.student_details_delete,
        name="student_details_delete",
    ),
    path(
        "stu_libary_surrender_card/<pk>",
        views.stu_libary_surrender_card,
        name="stu_libary_surrender_card",
    ),
    path("payment_method", views.payment_method, name="payment_method"),
    path("email_setting", views.email_setting, name="email_setting"),
    path("chat_index", views.chat_index, name="chat_index"),
    path("save_contact", views.save_contact, name="save_contact"),
    path("chat/<pk>", views.chat, name="chat"),
    path("chat_msg_save_js", views.chat_msg_save_js, name="chat_msg_save_js"),
    path("chat_view_js", views.chat_view_js, name="chat_view_js"),
    path("sms_setting", views.sms_setting, name="sms_setting"),
    path("send_sms", views.send_sms, name="send_sms"),
    path("indvidula_send_sms", views.indvidula_send_sms, name="indvidula_send_sms"),
    path("eventcalendar", views.eventcalendar, name="eventcalendar"),
    path("event_calendar_save", views.event_calendar_save, name="event_calendar_save"),
    path("eventcalendar_edit", views.eventcalendar_edit, name="eventcalendar_edit"),
    path(
        "event_calendar_delete",
        views.event_calendar_delete,
        name="event_calendar_delete",
    ),
    path(
        "calendarnofication_edit/<pk>",
        views.calendarnofication_edit,
        name="calendarnofication_edit",
    ),
    path(
        "calendarnofication_delete/<pk>",
        views.calendarnofication_delete,
        name="calendarnofication_delete",
    ),
    path("To_do_list", views.To_do_list, name="To_do_list"),
    path("student_user", views.student_user, name="student_user"),
    path("active_js", views.active_js, name="active_js"),
    path("active_parent_js", views.active_parent_js, name="active_parent_js"),
    path("active_staff_js", views.active_staff_js, name="active_staff_js"),
    path("custom_fields", views.custom_fields, name="custom_fields"),
    path(
        "custom_fields_edit/<pk>", views.custom_fields_edit, name="custom_fields_edit"
    ),
    path(
        "custom_fields_delete/<pk>",
        views.custom_fields_delete,
        name="custom_fields_delete",
    ),
    path("modules", views.modules, name="modules"),
    path("modules_parent", views.modules_parent, name="modules_parent"),
    path("modules_student", views.modules_student, name="modules_student"),
    path(
        "student_profile_update",
        views.student_profile_update,
        name="student_profile_update",
    ),
    path(
        "system_fields_student",
        views.system_fields_student,
        name="system_fields_student",
    ),
    path("system_fields_staff", views.system_fields_staff, name="system_fields_staff"),
    path(
        "student_doc_delete/<pk>", views.student_doc_delete, name="student_doc_delete"
    ),
    path(
        "delete_staff_document/<pk>",
        views.delete_staff_document,
        name="delete_staff_document",
    ),
    path(
        "delete_staff_timeline/<pk>",
        views.delete_staff_timeline,
        name="delete_staff_timeline",
    ),
    path("student_search", views.student_search, name="student_search"),
    path("print_header_footer", views.print_header_footer, name="print_header_footer"),
    path("print_fees/<pk>", views.print_fees, name="print_fees"),
    path("print_master_fees/<pk>", views.print_master_fees, name="print_master_fees"),
    path(
        "fees_carry_forward_save",
        views.fees_carry_forward_save,
        name="fees_carry_forward_save",
    ),
]
