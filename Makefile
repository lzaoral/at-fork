# Makefile for source rpm: at
# $Id$
NAME := at
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
