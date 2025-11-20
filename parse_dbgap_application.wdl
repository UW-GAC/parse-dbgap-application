version 1.0

workflow parse_dbgap_application {
    input {
        File application_pdf
    }
    call extract_dars {
        input: application_pdf=application_pdf
    }
    call render_report {
        input: dar_file=extract_dars.dar_file
    }
    output {
        File dar_file=extract_dars.dar_file
        File dar_report=render_report.dar_report
    }
    meta {
        author: "Adrienne Stilp"
        email: "amstilp@uw.edu"
    }
}


task extract_dars {
    input {
        File application_pdf
    }

    command {
        python /usr/local/parse-dbgap-application/parse_dars.py \
            ~{application_pdf} \
            dars.tsv
    }

    output {
        File dar_file = "dars.tsv"
    }

    runtime {
        docker: "uwgac/parse-dbgap-application:0.2.1"
    }
}


task render_report {
    input {
        File dar_file="dars.tsv"
    }
    command {
        cp /usr/local/parse-dbgap-application/dar_report.Rmd .
        R -e "rmarkdown::render('dar_report.Rmd', params=list(dar_file='~{dar_file}'))"
    }
    output {
        File dar_report = "dar_report.html"
    }
    runtime {
        docker: "uwgac/parse-dbgap-application:0.2.1"
    }
}
