cmake_minimum_required(VERSION 2.8.3)
project(roscompile)
find_package(catkin REQUIRED COMPONENTS
  rospack
  rospy
  resource_retriever
)
catkin_python_setup()
catkin_package(CATKIN_DEPENDS resource_retriever)
catkin_install_python(PROGRAMS scripts/roscompile scripts/convert_to_format_2 test/format_cmakes.py
                      DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
install(FILES stdeb.cfg .gitignore README.md DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
install(FILES
           data/cmake.ignore
           data/package.ignore
           data/cmake_patterns.ignore
           data/package_patterns.ignore
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/data)

if(CATKIN_ENABLE_TESTING)
  find_package(catkin REQUIRED COMPONENTS roslint)
  set(ROSLINT_PYTHON_OPTS --max-line-length=120 --ignore=E111,E114,E302)
  roslint_python()
  roslint_add_test()

  catkin_download_test_data(test_data.zip
      https://github.com/DLu/roscompile_test_data/raw/master/test_data.zip
      DESTINATION ${CATKIN_DEVEL_PREFIX}/${CATKIN_PACKAGE_SHARE_DESTINATION}/test
  )

endif()
